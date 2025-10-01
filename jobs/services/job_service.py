class JobService:
    def __init__(self, repository):
        self.repository = repository

    def create_job(self, title, description, company, location, recruiter, keywords):
        return self.repository.create_job(title, description, company, location, recruiter, keywords)

    def get_job(self, job_id):
        return self.repository.get_job_by_id(job_id)

    def list_jobs(self):
        return self.repository.list_jobs()