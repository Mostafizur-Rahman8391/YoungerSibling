from colorama import Fore
import dns.resolver

def email_lookup(email):
    print(Fore.CYAN + "\n[+] Performing Email Lookup...")
    try:
        domain = email.split("@")[-1]
        answers = dns.resolver.resolve(domain, 'MX')
        return {
            "Email": email,
            "MX Records": ", ".join([str(r.exchange) for r in answers]),
            "Domain": domain
        }
    except Exception as e:
        return {"Error": str(e)}