# Evidence Schema

Each finding contains an array of evidence objects.

## Evidence object

- `entry_id`: deterministic local identifier for the HAR entry
- `url`: request URL
- `method`: request method
- `vendor`: normalized vendor if identified
- `excerpt`: short, redacted excerpt from request data
- `matched_on`: list of rule triggers satisfied by this evidence
