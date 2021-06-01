## Authenticated API for HPI

Built on top of [HPI_API](https://github.com/seanbreckenridge/hpi_api/) and setup is largely taken from seanbreckenridge's work.

If you need an in-depth guide for how HPI_API works, I suggest going to the above repo so this repo doesn't duplicate documentation.

### Installation

```bash
pip install https://github.com/hpi/authenticated_hpi_api/
```

### Running

By default, HPI_API listens on port 5050.


```bash
auth_hpi_api server -k <public key, no headers> -i <JWT issuer>
```

### Examples

Example uses [https://github.com/madelinecameron/hpi](https://github.com/madelinecameron/hpi)

```bash
$ curl -H "Authorization: Bearer <jwt>" http://localhost:5050/my/eightsleep/sessions
{
  "page": 1,
  "limit": 50,
  "items": [
    {
      ...
    },
  ]
}

$ curl -H "Authorization: Bearer <bad jwt>" http://localhost:5050/my/eightsleep/sessions
{
  "error": "<error message>"
}
```
