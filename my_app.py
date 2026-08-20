from ion_language import parse_ion
from intent_system import create_api_intent, IntentVerifier

ast = parse_ion("intent Service: get / -> test()")
intent = create_api_intent('Service', [{'method': 'get', 'path': '/', 'function': 'test'}], [])
verifier = IntentVerifier()
status, proof = verifier.verify_intent(intent)
print(f"Verification: {status.value}")
