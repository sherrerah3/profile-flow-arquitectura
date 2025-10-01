from abc import ABC, abstractmethod

class JobRepository(ABC):
    @abstractmethod
    def create_job(self, title, description, company, location, recruiter, keywords):
        pass

    @abstractmethod
    def get_job_by_id(self, job_id):
        pass

    @abstractmethod
    def list_jobs(self):
        pass