from django.db import transaction
from .models import Commission, Job, JobApplication


class CommissionService:

    @staticmethod
    @transaction.atomic
    def create_commission(author, data, jobs_data):
        commission = Commission.objects.create(
            maker=author,
            **data
        )

        for job_data in jobs_data:
            Job.objects.create(
                commission=commission,
                **job_data
            )

        return commission

    @staticmethod
    def apply_to_job(applicant, job):
        if job.status == "FULL":
            raise ValueError("Job is already full")

        if JobApplication.objects.filter(
            job=job,
            applicant=applicant
        ).exists():
            raise ValueError("Already applied")

        application = JobApplication.objects.create(
            job=job,
            applicant=applicant
        )

        accepted_count = job.applications.filter(status="ACCEPTED").count()

        if accepted_count >= job.manpower_required:
            job.status = "FULL"
            job.save()

        return application

    @staticmethod
    def sync_commission_status(commission):
        jobs = commission.jobs.all()

        if all(job.status == "FULL" for job in jobs):
            commission.status = "FULL"
            commission.save()

    @staticmethod
    def get_commission_summary(commission):
        jobs = commission.jobs.all()

        total = sum(job.manpower_required for job in jobs)

        accepted = sum(
            job.applications.filter(status="ACCEPTED").count()
            for job in jobs
        )

        return {
            "total_manpower": total,
            "open_manpower": total - accepted,
        }