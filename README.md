# Thai Address Detection API

English | [ภาษาไทย](README.th.md)

Turn free-form Thai address text into structured fields with a dictionary-based FastAPI service. This is the rule-based version: it uses PyThaiNLP and reference address data rather than a transformer model.

## Quick start

From the repository root, run:

```bash
docker compose up --build
```

Open [Swagger UI](http://localhost:8000/docs) and try `POST /address-check` with this synthetic request:

```json
{"text":"ต.สุเทพ อ.เมืองเชียงใหม่ จ.เชียงใหม่ 50200"}
```

The response wraps the extracted fields in `address`: `province`, `amphoe` (district), `district` (subdistrict), `zipcode`, `name`, and `phone`. Results depend on the input and available reference data; sample outputs are not delivery guarantees.

## How it works

[The tagging pipeline](thaiAddressTag/tag.py) tokenizes Thai text, checks spelling against a custom dictionary, and matches candidate locations against [the reference list](thaiAddressTag/addresses.py). [The API entry point](main.py) also runs locally with Python 3.11 after installing [`requirements.txt`](requirements.txt): `python main.py`.

See the [companion notebook](https://github.com/ffe111/thaiAddressTag) for the underlying approach, or the [transformer-based API](https://github.com/ffe111/thai_addr_dt) for a different implementation. When reporting an extraction issue, use a synthetic example rather than a real name, phone number, or address.

<!-- Maintainers: Update the English README first, then mirror the change in README.th.md. -->
