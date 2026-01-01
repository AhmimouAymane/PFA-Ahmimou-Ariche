"""
Script to seed the database with Moroccan administrative documents
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from database import db
from models.document import Document

def seed_documents():
    """Seed database with sample Moroccan administrative documents"""
    app = create_app()
    
    with app.app_context():
        # Check if documents already exist
        if Document.query.count() > 0:
            print("Documents already exist. Skipping seed.")
            return
        
        documents = [
            # French documents
            {
                "title": "Comment obtenir une carte d'identité nationale",
                "content": """Pour obtenir une carte d'identité nationale au Maroc, vous devez vous rendre à la préfecture ou sous-préfecture de votre lieu de résidence avec les documents suivants:

1. Une copie de l'acte de naissance (extrait de naissance)
2. Deux photos d'identité récentes (format 3.5 x 4.5 cm)
3. Un justificatif de résidence (facture d'eau, d'électricité ou attestation d'hébergement)
4. L'ancienne carte d'identité si c'est un renouvellement
5. Une copie de la carte d'identité du père ou du tuteur légal

Le délai de délivrance est généralement de 30 jours. Le coût est de 50 dirhams pour la première délivrance et 25 dirhams pour le renouvellement.""",
                "language": "fr",
                "category": "identity"
            },
            {
                "title": "Comment obtenir un passeport marocain",
                "content": """Pour obtenir un passeport marocain, vous devez:

1. Remplir le formulaire de demande de passeport
2. Fournir les documents suivants:
   - Copie de la carte d'identité nationale
   - Copie de l'acte de naissance
   - Deux photos d'identité récentes (format 3.5 x 4.5 cm)
   - Justificatif de résidence
   - Ancien passeport (si renouvellement)
3. Payer les frais: 300 dirhams pour un passeport de 10 ans

Vous pouvez faire la demande en ligne sur le portail www.passeport.ma ou vous rendre à la préfecture.""",
                "language": "fr",
                "category": "passport"
            },
            {
                "title": "Comment obtenir un certificat de résidence",
                "content": """Le certificat de résidence est délivré par la commune ou la préfecture. Pour l'obtenir:

1. Remplir le formulaire de demande
2. Fournir:
   - Copie de la carte d'identité nationale
   - Justificatif de résidence (facture d'eau, d'électricité, contrat de location)
   - Deux photos d'identité
3. Délai: 3 à 7 jours
4. Coût: 10 dirhams

Le certificat de résidence est valable 3 mois.""",
                "language": "fr",
                "category": "certificates"
            },
            {
                "title": "Comment obtenir un extrait de casier judiciaire",
                "content": """L'extrait de casier judiciaire peut être obtenu:

1. En ligne sur www.casierjudiciaire.ma
2. En se rendant au tribunal de première instance
3. Documents requis:
   - Copie de la carte d'identité nationale
   - Formulaire de demande rempli
4. Délai: 1 à 2 semaines
5. Coût: 10 dirhams

L'extrait est valable 3 mois.""",
                "language": "fr",
                "category": "certificates"
            },
            
            # Arabic documents
            {
                "title": "كيفية الحصول على بطاقة التعريف الوطنية",
                "content": """للحصول على بطاقة التعريف الوطنية في المغرب، يجب التوجه إلى عمالة أو إقليم مكان الإقامة مع الوثائق التالية:

1. نسخة من عقد الولادة (مستخرج من السجل المدني)
2. صورتان شمسيتان حديثتان (مقاس 3.5 × 4.5 سم)
3. إثبات السكن (فاتورة الماء أو الكهرباء أو شهادة الإقامة)
4. البطاقة القديمة إذا كان الأمر يتعلق بالتجديد
5. نسخة من بطاقة تعريف الأب أو الوصي القانوني

مدة التسليم عادة 30 يوما. التكلفة هي 50 درهما للإصدار الأول و 25 درهما للتجديد.""",
                "language": "ar",
                "category": "identity"
            },
            {
                "title": "كيفية الحصول على جواز السفر المغربي",
                "content": """للحصول على جواز السفر المغربي، يجب:

1. ملء استمارة طلب جواز السفر
2. تقديم الوثائق التالية:
   - نسخة من بطاقة التعريف الوطنية
   - نسخة من عقد الولادة
   - صورتان شمسيتان حديثتان (مقاس 3.5 × 4.5 سم)
   - إثبات السكن
   - جواز السفر القديم (في حالة التجديد)
3. دفع الرسوم: 300 درهم لجواز سفر صالح لمدة 10 سنوات

يمكن تقديم الطلب عبر الإنترنت على الموقع www.passeport.ma أو التوجه إلى العمالة.""",
                "language": "ar",
                "category": "passport"
            },
            
            # English documents
            {
                "title": "How to obtain a national identity card",
                "content": """To obtain a national identity card in Morocco, you must go to the prefecture or sub-prefecture of your place of residence with the following documents:

1. A copy of the birth certificate (extract from civil registry)
2. Two recent identity photos (3.5 x 4.5 cm format)
3. Proof of residence (water bill, electricity bill, or accommodation certificate)
4. Old identity card if renewal
5. A copy of the father's or legal guardian's identity card

The delivery time is generally 30 days. The cost is 50 dirhams for first issue and 25 dirhams for renewal.""",
                "language": "en",
                "category": "identity"
            },
        ]
        
        for doc_data in documents:
            doc = Document(**doc_data)
            db.session.add(doc)
        
        db.session.commit()
        print(f"Seeded {len(documents)} documents successfully!")

if __name__ == '__main__':
    seed_documents()

