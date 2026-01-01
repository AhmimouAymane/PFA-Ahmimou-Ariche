from llm.translation_service import TranslationService
from llm.local_model_service import LocalModelService

ts = TranslationService()
lms = LocalModelService()

def debug_flow(q, lang):
    print(f"\n--- User ({lang}): {q} ---")
    fr = ts.translate(q, lang, 'fr')
    print(f"Translated to French: '{fr}'")
    
    # Check what would match in LMS
    match = None
    fr_lower = fr.lower()
    for keyword_group in lms.keywords_to_check: # I'll need to make this accessible or just mock it
        for kw in keyword_group:
            if kw in fr_lower:
                match = keyword_group[0]
                break
        if match: break
    
    print(f"LMS Match: {match if match else 'DEFAULT'}")
    resp = lms.generate_response("", fr)
    print(f"Response Preview: {resp[:50]}...")

if __name__ == "__main__":
    # Add keywords to lms object for testing (it was private in my thought but I'll add it in real code or use a copy)
    lms.keywords_to_check = [
        ("carte d'identité", "cnie", "identité"),
        ("passeport",),
        ("naissance", "certificat de naissance"),
        ("permis", "conduire", "permis de conduire"),
        ("carte grise", "immatriculation"),
        ("casier judiciaire", "casier"),
        ("résidence", "certificat de résidence"),
        ("mariage", "zawaj"),
        ("divorce",),
        ("succession", "héritage"),
        ("logement social", "logement", "lkouacem"),
        ("ramed",),
        ("cnss", "sécurité sociale"),
        ("marché public", "appel d'offres"),
        ("aide", "tayssir", "daam"),
        ("visa",),
        ("bourse", "études"),
    ]
    
    debug_flow("جواز سفر", "ar")
    debug_flow("بطاقة التعريف", "ar")
    debug_flow("رخصة السياقة", "ar")
    debug_flow("عقد الزواج", "ar")
    debug_flow("Passeport", "fr")
    debug_flow("Permis", "fr")
