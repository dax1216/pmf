from celery import shared_task

from .ai import evaluate_company_pmf_salesforce


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=1, max_retries=3)
def run_pmf_score(self, company_id):
    evaluate_company_pmf_salesforce(company_id)
