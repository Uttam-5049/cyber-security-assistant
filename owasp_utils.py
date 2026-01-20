import requests
import logging
from bs4 import BeautifulSoup
from langchain.docstore.document import Document

def fetch_owasp_cheatsheets():
    base_url = "https://cheatsheetseries.owasp.org/"
    scraped_docs = []
    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.select("a[href^='cheatsheets/']")
        for link in links[:5]:
            title = link.text.strip()
            href = link.get("href")
            full_url = f"{base_url}{href}"
            try:
                page = requests.get(full_url, timeout=10)
                page.raise_for_status()
                text = BeautifulSoup(page.text, "html.parser").get_text()
                scraped_docs.append(Document(page_content=f"{title}\n{text}"))
                               
                print(f"[OWASP] Scraped cheat sheet: {title} → {full_url}")
                with open("metrics_logs/test_log.txt", "a", encoding="utf-8") as logf:
                    logf.write(f"[OWASP] Scraped cheat sheet: {title} → {full_url}\n")
            except Exception as e:
                logging.error(f"Failed to load cheat sheet {title}: {e}")
    except Exception as e:
        logging.error(f"OWASP fetch failed: {e}")
    return scraped_docs
