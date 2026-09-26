from guardrails import Guard
from guardrails_ai.detect_pii import DetectPII
from guardrails_ai.secrets_present import SecretsPresent


class PrivacyGuard:
    def __init__(self):
        self.pii = Guard().use(DetectPII, on_fail="fix")
        self.secrets = Guard().use(SecretsPresent, on_fail="fix")

    @staticmethod
    def _value(result, fallback: str) -> str:
        return getattr(result, "validated_output", None) or fallback

    def sanitize(self, text: str) -> str:
        pii_result = self.pii.validate(text)
        pii_safe = self._value(pii_result, text)
        secret_result = self.secrets.validate(pii_safe)
        return self._value(secret_result, pii_safe)
