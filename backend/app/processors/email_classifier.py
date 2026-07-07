import re


class EmailClassifier:

    RECRUITER_DOMAINS = {
        "linkedin.com": "LinkedIn",
        "indeed.com": "Indeed",
        "greenhouse.io": "Greenhouse",
        "greenhouse-mail.io": "Greenhouse",
        "lever.co": "Lever",
        "ashbyhq.com": "Ashby",
        "smartrecruiters.com": "SmartRecruiters",
        "workday.com": "Workday",
    }

    CATEGORY_RULES = {
        "Offer": [
            "job offer",
            "offer letter",
            "offer for",
            "employment offer",
        ],
        "Interview": [
            "interview",
            "schedule interview",
            "interview invitation",
            "meet with",
        ],
        "Assessment": [
            "assessment",
            "coding challenge",
            "hackerrank",
            "codility",
            "testgorilla",
            "online test",
            "technical assessment",
        ],
        "Rejection": [
            "unfortunately",
            "we regret",
            "not selected",
            "other candidates",
            "position has been filled",
        ],
        "Application": [
            "application received",
            "thank you for applying",
            "application confirmation",
            "we received your application",
        ],
        "Recruiter": [
            "opportunity",
            "your background",
            "your profile",
            "would like to connect",
            "interesting opportunity",
        ],
    }

    IGNORE_KEYWORDS = [
        "unsubscribe",
        "promotion",
        "receipt",
        "invoice",
        "order shipped",
        "password reset",
        "verify your email",
        "security alert",
        "newsletter",
        "amazon.ca",
        "amazon.com",
        "paypal",
        "spotify",
        "netflix",
    ]

    def classify(self, email: dict) -> dict:

        subject = (email.get("subject") or "").lower()
        sender = (email.get("from") or "").lower()
        body = (email.get("body") or "").lower()
        snippet = (email.get("snippet") or "").lower()

        text = f"{subject}\n{snippet}\n{body}"

        #
        # Ignore obvious non-job emails
        #
        for keyword in self.IGNORE_KEYWORDS:

            if keyword in text:
                return {
                    "is_job_related": False,
                    "category": "Ignored",
                    "source": None,
                    "confidence": 100,
                    "matched_rule": keyword,
                }

        #
        # Detect email source
        #
        source = None

        for domain, name in self.RECRUITER_DOMAINS.items():

            if domain in sender:
                source = name
                break

        #
        # Detect category
        #
        for category, keywords in self.CATEGORY_RULES.items():

            for keyword in keywords:

                if keyword in text:
                    return {
                        "is_job_related": True,
                        "category": category,
                        "source": source,
                        "confidence": 95,
                        "matched_rule": keyword,
                    }

        #
        # Generic recruiter detection
        #
        recruiter_words = [
            "recruiter",
            "talent",
            "hiring",
            "careers",
            "career",
            "human resources",
            "hr",
        ]

        if any(word in text for word in recruiter_words):
            return {
                "is_job_related": True,
                "category": "Recruiter",
                "source": source,
                "confidence": 80,
                "matched_rule": "generic recruiter",
            }

        #
        # Nothing matched
        #
        return {
            "is_job_related": False,
            "category": "Unknown",
            "source": source,
            "confidence": 0,
            "matched_rule": None,
        }
