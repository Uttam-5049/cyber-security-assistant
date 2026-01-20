from sentence_transformers import SentenceTransformer, util
from collections import Counter

chat_data = [
    # this is from history.json so we can just copy and paste content of that file
{
    "type": "human",
    "content": "what is sql injection?"
  },
  {
    "type": "ai",
    "content": "  SQL injection is a code injection technique that might destroy your database. It is one of the most common web hacking techniques. This is done by placing malicious SQL statements in input fields. To prevent it, use prepared statements and parameterized queries."
  },
  {
    "type": "human",
    "content": "what is ajax security?"
  },
  {
    "type": "ai",
    "content": "  AJAX security is the practice of implementing secure methods for using Asynchronous JavaScript and XML (AJAX) in web application development to prevent attacks such as cross-site scripting (XSS), SQL injection, and other injection style issues. It includes guidelines on how to properly encode data before use in an output context, avoid writing serialization code, and avoid building dynamic XML or JSON."
  },
  {
    "type": "human",
    "content": "What is the CVE database?"
  },
  {
    "type": "ai",
    "content": "  CVE stands for Common Vulnerabilities and Exposures. It is a publicly-available database of information security vulnerabilities maintained by Mitre Corporation. The database includes descriptions of the vulnerability, its impact, likelihood of occurrence, and references to resources that can help mitigate or exploit it. CVEs are used in a variety of contexts, including vulnerability assessments, penetration testing, and software development. They are often used as part of automated tools to identify known vulnerabilities in systems and applications."
  },
  {
    "type": "human",
    "content": "how does it helps to identify vulnerabilities?"
  },
  {
    "type": "ai",
    "content": "\nThe CVE database helps to identify vulnerabilities in a number of ways. \nFirst, the CVE (Common Vulnerability Scoring System) is a standard for scoring and assessing the risk of vulnerabilities. \nThis standard assigns scores between 0 and 9 (1 being high severity \nand 9 being low severity) to each vulnerability. \n\nThe CVE database provides information on known vulnerabilities and their scores, allowing for better prioritization \nof patching efforts. It also provides information on exploits for each vulnerability, helping to identify which vulnerabilities \nare actively being targeted by threat actors. This can help security teams prioritize patching efforts based on the likelihood \nthat an attack will occur and the potential damage that could be caused. \n\nThe CVE database also allows for better understanding of how different vulnerabilities relate to each other, \nand what impact they may have together. This can be especially useful when assessing the impact of a larger vulnerability \nHow does the CVE database help to identify vulnerabilities?"
  },
  {
    "type": "human",
    "content": "What is Cross-Site Scripting (XSS)?"
  },
  {
    "type": "ai",
    "content": " Cross-Site Scripting (XSS) is a type of coding vulnerability that allows attackers to inject malicious code into web pages viewed by other users. It can lead to serious security risks and is one of the most common vulnerabilities found in web applications according to OWASP Top 10. There are three types of XSS: Reflected XSS (Non-Persistent), Stored XSS (Persistent), and DOM based XSS. To prevent XSS attacks, it's important to properly encode untrusted data and use one of the APIs provided for introducing untrusted data into the DOM. Tools like ZAP can help automate the process of finding and removing XSS vulnerabilities, but manual code reviews are also important in order to catch any that automated tools may miss."
  },
  {
    "type": "human",
    "content": "What is two-factor authentication (2FA)?\n"
  },
  {
    "type": "ai",
    "content": " Two-factor authentication (2FA) is a security measure in which a person provides two different authentication factors to verify their identity before being allowed access. These factors can include something the user knows, such as a password or PIN, something the user has, such as a token or mobile phone, and/or something the user is, such as a biometric factor like a fingerprint or facial recognition. Two-factor authentication is considered a more secure way of verifying identity than just using a single factor because it requires the attacker to compromise two different layers of security rather than just one."
  },
  {
    "type": "human",
    "content": "How does a firewall protect a network?"
  },
  {
    "type": "ai",
    "content": " Firewalls play an important role in network security as they protect against hackers and viruses. They can also safeguard the structure and addressing scheme of a network from outside threats. There are three types of firewalls: static-packet filtering, circuit-level gateway, and application-layer firewall. Firewalls can be hardware devices or software applications that filter both incoming and outgoing traffic to allow only data that has been personally requested. It is important to choose a firewall with features such as inbound and outbound filtering, stealth mode, notifications, and application protection for optimal security."
  },
  {
    "type": "human",
    "content": "What is phishing?\n"
  },
  {
    "type": "ai",
    "content": "  Phishing is the practice of attempting to trick individuals into divulging sensitive information (such as login credentials or credit card numbers) under false pretenses. This is typically done through email, text messages, phone calls, or other forms of communication that appear to be legitimate but are actually designed to deceive the recipient. Phishing can take many forms, such as phishing emails, fake websites, and even social media scams, and can be used by cybercriminals, hackers, or even legitimate organizations for a variety of purposes, including identity theft, financial fraud, and espionage. To protect yourself against phishing attacks, it's important to stay vigilant, verify the authenticity of any suspicious communications or websites, and never click on links or download attachments from unknown or unverified sources."
  },
  {
    "type": "human",
    "content": "What is encryption?"
  },
  {
    "type": "ai",
    "content": "  Encryption is the process of converting plaintext, which is sensitive data or information, into ciphertext using a mathematical algorithm and an encryption key. It is a security service that cryptography provides to safeguard information from unauthorized individuals by ensuring confidentiality (that the message sent is for the intended receiver only) and integrity (guaranteeing that the content of the message is not tempered or changed in any way)."
  }
]

reference_answers = [
    "SQL injection is a web security vulnerability where attackers insert malicious SQL commands through user input to manipulate databases.",
    "AJAX security involves securing asynchronous JavaScript requests to prevent common attacks such as cross-site scripting (XSS) and cross-site request forgery (CSRF).",
    "The CVE database is a centralized repository of publicly known cybersecurity vulnerabilities maintained by MITRE.",
    "The CVE system helps identify vulnerabilities by assigning unique identifiers to known security issues, allowing organizations and security professionals to track, share, and address these vulnerabilities consistently across different tools and platforms.",
    "Cross-Site Scripting (XSS) is a security vulnerability that allows attackers to inject malicious scripts into webpages viewed by other users.",
    "Two-factor authentication (2FA) adds an extra layer of security by requiring a second form of verification beyond just a password.",
    "A firewall protects a network by filtering incoming and outgoing traffic based on security rules, blocking unauthorized access.",
    "Phishing is a cyber attack that uses deceptive emails or websites to trick people into revealing sensitive information like passwords or credit card numbers.",
    "Encryption is the process of converting data into a coded form to prevent unauthorized access during transmission or storage."
]

qa_pairs = []
for i in range(len(chat_data)-1):
    if chat_data[i]['type'] == 'human' and chat_data[i+1]['type'] == 'ai':
        qa_pairs.append({
            "question": chat_data[i]['content'].strip(),
            "predicted": chat_data[i+1]['content'].strip()
        })

samples = []
for i, pair in enumerate(qa_pairs):
    samples.append({
        "question": pair['question'],
        "predicted": pair['predicted'],
        "reference": reference_answers[i]
    })

model = SentenceTransformer('all-MiniLM-L6-v2')

def bert_similarity(predicted: str, reference: str) -> float:
    emb1 = model.encode(predicted, convert_to_tensor=True)
    emb2 = model.encode(reference, convert_to_tensor=True)
    cosine_sim = util.pytorch_cos_sim(emb1, emb2).item()
    return cosine_sim

def f1_token_level(predicted: str, reference: str) -> float:
    pred_tokens = predicted.lower().split()
    ref_tokens = reference.lower().split()

    pred_counter = Counter(pred_tokens)
    ref_counter = Counter(ref_tokens)

    common = pred_counter & ref_counter
    num_same = sum(common.values())

    if num_same == 0:
        return 0.0

    precision = num_same / len(pred_tokens)
    recall = num_same / len(ref_tokens)
    f1 = 2 * precision * recall / (precision + recall)
    return f1

def evaluate(samples):
    total_bert_sim = 0
    total_f1 = 0
    n = len(samples)

    for sample in samples:
        predicted = sample['predicted']
        reference = sample['reference']

        sim = bert_similarity(predicted, reference)
        f1 = f1_token_level(predicted, reference)

        total_bert_sim += sim
        total_f1 += f1

        print(f"Q: {sample['question']}")
        print(f"Predicted: {predicted}")
        print(f"Reference: {reference}")
        print(f"BERT similarity: {sim:.3f}, F1 score: {f1:.3f}\n")

    print("=== Summary ===")
    print(f"Average BERT similarity: {total_bert_sim / n:.3f}")
    print(f"Average F1 score: {total_f1 / n:.3f}")

if __name__ == "__main__":
    evaluate(samples)