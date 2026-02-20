# import re

# def extract_entities(text):
#     entities = {
#         "Name": [],
#         "Job Title": [],
#         "Address": [],
#         "Phone": [],
#         "Email": [],
#         "Website": []
#     }

#     # Email
#     emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
#     entities["Email"].extend(set(emails))

#     # Phone (international formats)
#     phones = re.findall(r"\+?\d{1,3}[\s\-]?\(?\d{2,4}\)?[\s\-]?\d{3,5}[\s\-]?\d{3,5}", text)
#     normalized_phones = [re.sub(r"[^\d+]", "", p) for p in phones]
#     entities["Phone"].extend(set(normalized_phones))

#     # Website (strict separation from emails)
#     websites = re.findall(r"(https?://[^\s]+|www\.[^\s]+|\b[A-Za-z0-9-]+\.[A-Za-z]{2,}(?:/[^\s]*)?)", text)
#     websites = [w for w in websites if "@" not in w]
#     entities["Website"].extend(set(websites))

#     # Address heuristic (capture full lines including postal codes)
#     address_lines = []
#     for line in text.splitlines():
#         if any(keyword in line.lower() for keyword in [
#             "street","road","city","state","zip","avenue","blvd","boulevard",
#             "plaza","lane","sector","block","district","county","village",
#             "pincode","postal","code"
#         ]) or re.search(r"\d{5,6}", line):  # catch numeric postal codes inline
#             address_lines.append(line.strip())
#     if address_lines:
#         entities["Address"].append(" ".join(address_lines))

#     # Job Title heuristic
#     job_titles = []
#     for line in text.splitlines():
#         if any(title in line.lower() for title in [
#             "manager","engineer","developer","designer","director","consultant",
#             "analyst","lead","specialist","executive","founder","ceo","cto","cfo",
#             "officer","architect","sales","marketing","principal"
#         ]):
#             job_titles.append(line.strip())
#     entities["Job Title"].extend(set(job_titles))

#     # Name heuristic (first clean line without digits/symbols)
#     for line in text.splitlines():
#         if line.strip() and not re.search(r"\d|@|www|\.com", line.lower()):
#             entities["Name"].append(line.strip())
#             break

#     return entities


import re

def extract_entities(text):
    entities = {
        "Name": [],
        "Job Title": [],
        "Address": [],
        "Phone": [],
        "Email": [],
        "Website": []
    }

    # Email
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    entities["Email"].extend(set(emails))

    # Phone (international formats)
    phones = re.findall(r"\+?\d{1,3}[\s\-]?\(?\d{2,4}\)?[\s\-]?\d{3,5}[\s\-]?\d{3,5}", text)
    normalized_phones = [re.sub(r"[^\d+]", "", p) for p in phones]
    entities["Phone"].extend(set(normalized_phones))

    # Website
    websites = re.findall(r"(https?://[^\s]+|www\.[^\s]+|\b[A-Za-z0-9-]+\.[A-Za-z]{2,}(?:/[^\s]*)?)", text)
    websites = [w for w in websites if "@" not in w]
    entities["Website"].extend(set(websites))

    # Address
    address_lines = []
    for line in text.splitlines():
        if any(keyword in line.lower() for keyword in [
            "street","road","city","state","zip","avenue","blvd","boulevard",
            "plaza","lane","sector","block","district","county","village",
            "pincode","postal","code"
        ]) or re.search(r"\d{5,6}", line):
            address_lines.append(line.strip())
    entities["Address"].extend(set(address_lines))

    # Job Title
    job_keywords = [
        "manager","engineer","developer","designer","director","consultant",
        "analyst","lead","specialist","executive","founder","ceo","cto","cfo",
        "officer","architect","sales","marketing","principal"
    ]
    job_titles = []
    for line in text.splitlines():
        if re.search(r"\b(" + "|".join(job_keywords) + r")\b", line.lower()):
            job_titles.append(line.strip())
    entities["Job Title"].extend(set(job_titles))

    # Name
    for line in text.splitlines():
        if line.strip() and not re.search(r"\d|@|www|\.com", line.lower()):
            if not re.search(r"(inc|ltd|llc|company)", line.lower()):
                entities["Name"].append(line.strip())
                break

    return entities