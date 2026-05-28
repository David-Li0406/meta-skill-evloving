## Installations (end-user flows)

An "end-user flow" is a flow intended to be used by others in the workspace.
In MVP, a flow becomes end-user facing by adding the `:end-user` tag to `:tags`.

An "installation" is a per-user instance of an end-user flow, backed by a prod
profile (`:profile-type :prod`) owned by the subscribing user.

### Creator: declare activation inputs (setup form)

Installation setup inputs are declared via `:requires` with a `{:kind :form ...}`
requirement. These values are stored on the installation as `:activation-inputs`
and merged into runs as `:activation` input.

Example:

```clojure
{:tags [:end-user]
 :requires [{:kind :form
             :label "Setup"
             :fields [{:key :region
                       :label "Region"
                       :field-type :select
                       :required true
                       :options ["EU" "US"]}]}]}
```

### Creator: declare per-run inputs for webhook/manual triggers

For triggers that should drive a generic UI/CLI (like an upload form), declare
optional trigger `:config :fields`.

Fields are validated and coerced on receipt (for webhooks) and can be used to:
- tell the UI/CLI which inputs to ask for
- support multi-file uploads via `:multiple true`

Example (webhook upload):

```clojure
{:triggers [{:type :event
             :label "Upload"
             :enabled true
             :config {:source :webhook
                      :event-name "files.upload"
                      :auth {:type :hmac-sha256
                             :header "X-Signature"
                             :secret-ref :webhook-secret}
                      :fields [{:name :files
                                :type :file
                                :required true
                                :multiple true}]}}]}
```

Notes:
- `:type :file`, `:blob`, and `:blob-ref` are treated as `:blob-ref` in validation.
- When the request is multipart, flows-api persists file parts and passes them
  to the flow as blob-ref maps (e.g. `{:path \"...\" :size-bytes 123 ...}`).

### End user: subscribe + activate (CLI)

```bash
# 1) Create installation (disabled by default)
breyta flows installations create <flow-slug> --name "My setup"

# 2) Provide activation inputs (from :requires form fields)
breyta flows installations set-inputs <profile-id> --input '{"region":"EU"}'

# 3) Enable (activate) the installation
breyta flows installations enable <profile-id>
```

### End user: upload files (CLI)

1) Inspect installation triggers and their webhook endpoints:

```bash
breyta flows installations triggers <profile-id>
```

2) Upload one or more files to the installation’s webhook trigger:

```bash
breyta flows installations upload <profile-id> --file ./a.pdf --file ./b.pdf
```

If the trigger declares exactly one webhook field of type `file`/`blob`/`blob-ref`,
the CLI infers the multipart field name automatically; otherwise pass it:

```bash
breyta flows installations upload <profile-id> --file-field files --file ./a.pdf
```
