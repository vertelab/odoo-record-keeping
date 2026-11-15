# odoo-record-keeping — gren 19.0

> **Denna gren är avsiktligt tom.** Modulerna är INTE portade till Odoo 19.
> Grenen finns så att dev-miljöer (`hansolo19`) kan klona den utan att falla,
> men den påstår ingenting om att koden är portad.

## Baseline

| | |
|---|---|
| Källa | `20.0` |
| Moduler | **16** |
| Grenar i repot | `14.0`, `14.0-add-link-button`, `16.0`, `17.0`, `18.0`, `20.0`, `main` |

## Moduler

- `record_keeping`
- `record_keeping_account`
- `record_keeping_agreement`
- `record_keeping_attachment`
- `record_keeping_classification`
- `record_keeping_dms`
- `record_keeping_event`
- `record_keeping_helpdesk`
- `record_keeping_hr`
- `record_keeping_im`
- `record_keeping_mail_channel`
- `record_keeping_project`
- `record_keeping_property_mgmt`
- `record_keeping_sale`
- `record_keeping_sale_project`
- `record_keeping_wizard`

## Blockerare

✅ Inga externa beroenden saknas i Odoo 19-kärnan eller OCA 19.0.

Modulerna kan troligen portas utan att vänta på externa bidrag.

## Nästa steg

Portering sker på `*-pfile`-maskin med versionsagnostisk kod
(`.p.py` / `.p.xml`). Se `/skill:odoo-pfiles`.
