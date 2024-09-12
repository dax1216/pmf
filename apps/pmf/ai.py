from django.template.loader import render_to_string
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from .models import Company, ProcessStatus


def pmf_score_criteria():
    properties = {
        "business_fit": {
            "type": "integer",
            "description": render_to_string("pmf/ai/properties/business_fit.txt", {}),
        },
        "customization": {
            "type": "integer",
            "description": render_to_string("pmf/ai/properties/customization.txt", {}),
        },
        "ease_of_adoption": {
            "type": "integer",
            "description": render_to_string(
                "pmf/ai/properties/ease_of_adoption.txt", {}
            ),
        },
        "cost": {
            "type": "integer",
            "description": render_to_string("pmf/ai/properties/cost.txt", {}),
        },
        "integration": {
            "type": "integer",
            "description": render_to_string("pmf/ai/properties/integration.txt", {}),
        },
    }
    return [
        {
            "name": "pmf_score_criteria",
            "description": "Evaluate the score per criteria based on the company information",
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": [
                    "business_fit",
                    "customization",
                    "ease_of_adoption",
                ],
            },
        }
    ]


def evaluate_company_pmf_salesforce(company_id):
    company = Company.objects.get(id=company_id)
    company.status = ProcessStatus.IN_PROGRESS
    company.save()

    prompt = PromptTemplate(
        template=render_to_string(
            "pmf/ai/company.txt", context={"company": company.name}
        ),
        input_variables=[],
    )
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0.2, max_tokens=2054)

    chain = prompt | llm
    company_info = chain.invoke({})

    # If the company is not found, no PMF evaluation is done
    if "Sorry, I could not find" in company_info.content:
        company.status = ProcessStatus.FAILED
        company.save()
        return company

    prompt = PromptTemplate(
        template=render_to_string("pmf/ai/context.txt"),
        input_variables=[],
    )

    chain = (
        prompt
        | llm.bind(
            function_call={"name": "pmf_score_criteria"}, functions=pmf_score_criteria()
        )
        | JsonOutputFunctionsParser()
    )

    scores = chain.invoke({"company_data": company_info.content})

    company.pmf_score_details = scores
    company.status = ProcessStatus.COMPLETED
    company.save()
    return company
