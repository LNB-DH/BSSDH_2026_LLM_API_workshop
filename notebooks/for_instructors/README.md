# Instructor Notebooks

These notebooks are for workshop organizers who need to prepare and distribute
participant API keys. They are not participant exercises.

## Notebooks

- `provision_open_router_keys.ipynb` creates OpenRouter API keys for workshop
  participants using an OpenRouter provisioning key.
- `email_participants_keys.ipynb` reads the provisioned participant spreadsheet
  and sends each participant their assigned API key through SendGrid.

## Required Private Inputs

Set these values outside the notebooks, for example as environment variables:

- `OPEN_ROUTER_BSSDH_PROVISIONER` - OpenRouter provisioning/admin key.
- `SENDGRID_API` - SendGrid API key.
- `SENDGRID_FROM_EMAIL` - verified sender address for SendGrid.

Participant spreadsheets and generated key files should stay in a local `temp`
folder. The repository ignores the likely temp locations used by these notebooks.

## Security Notes

- Do not commit participant spreadsheets, generated key JSON files, provisioned
  key spreadsheets, `.env` files, or executed notebook outputs.
- Clear notebook outputs before committing changes.
- Do not print API keys, participant emails, or participant table rows in cells
  whose outputs may be saved.
- Review dates, repository links, email subject lines, and message text before
  sending mail for a new workshop year.
