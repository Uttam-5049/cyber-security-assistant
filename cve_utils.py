import requests
import logging
from config import NVD_API_KEY

def fetch_cve_docs(keywords=["SQL injection"], max_results=5):
    cve_docs = []
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    headers = {
        "User-Agent": "MyCVEFetcher/1.0 (myemail@example.com)",
        "apiKey": NVD_API_KEY
    }
    for keyword in keywords:
        params = {
            "keywordSearch": keyword,
            "resultsPerPage": max_results,
            "startIndex": 0
        }
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            vulnerabilities = data.get("vulnerabilities", [])
            for item in vulnerabilities:
                cve = item.get("cve", {})
                cve_id = cve.get("id", "Unknown ID")
                descriptions = cve.get("descriptions", [])
                description = "No description available."
                for d in descriptions:
                    if d.get("lang") == "en":
                        description = d.get("value")
                        break
                doc_text = f"CVE ID: {cve_id}\nDescription: {description}"
                cve_docs.append(doc_text)
        except requests.exceptions.RequestException as e:
            logging.error(f"[CVE] Fetch failed for '{keyword}': {e}")
    return cve_docs

def fetch_cve_from_nvd_by_id(cve_id):
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    headers = {"User-Agent": "MyCVEFetcher/1.0 (myemail@example.com)"}
    params = {"apiKey": NVD_API_KEY, "cveId": cve_id}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        vulnerabilities = data.get("vulnerabilities", [])
        if not vulnerabilities:
            return {"description": "CVE not found or failed to fetch."}
        cve = vulnerabilities[0].get("cve", {})
        descriptions = cve.get("descriptions", [])
        description = "No description available."
        for d in descriptions:
            if d.get("lang") == "en":
                description = d.get("value")
                break
        impact = vulnerabilities[0].get("cve", {}).get("metrics", {})
        severity = "UNKNOWN"
        score = 0.0
        cvss_v3 = impact.get("cvssMetricV31") or impact.get("cvssMetricV30") or []
        if cvss_v3:
            cvss_info = cvss_v3[0].get("cvssData", {})
            severity = cvss_info.get("baseSeverity", "UNKNOWN")
            score = cvss_info.get("baseScore", 0.0)
        references_data = cve.get("references", {}).get("reference_data", [])
        references = [ref.get("url") for ref in references_data if ref.get("url")]
        return {
            "cve_id": cve_id,
            "description": description,
            "severity": severity,
            "score": score,
            "references": references
        }
    except requests.HTTPError as http_err:
        return {"description": f"HTTP error occurred: {http_err}"}
    except requests.RequestException as req_err:
        return {"description": f"Request error occurred: {req_err}"}
    except Exception as e:
        return {"description": f"Unexpected error: {e}"}
