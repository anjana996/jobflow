# JF-6 — Greenhouse discovery and submission feasibility

Research performed 25 October 2026. No application was submitted and no
applicant data was sent.

## Decision

- **Discovery: conditional go.** Greenhouse Job Board API GET endpoints are
  public and suitable for polling explicitly configured employer board tokens.
  This is not a universal Greenhouse job search: each employer board must be
  selected and configured separately.
- **API submission: no-go.** The submission endpoint requires an employer's
  secret Job Board API key. JobFlow does not have employer-issued credentials
  and must not infer that public listing access grants submission access.
- **Current fallback: manual handoff.** Preserve each job's `absolute_url`,
  inspect missing required answers, and send the user to the employer-hosted
  application form. A later submission adapter remains blocked until a target
  employer explicitly authorizes API access.

## Capability matrix

| Capability | Access and contract | Observed evidence | Decision |
| --- | --- | --- | --- |
| List public jobs | `GET /v1/boards/{board_token}/jobs`; no authentication; optional `content=true` | Board `aperaaiinc` returned HTTP 200, 9 jobs and `meta.total=9` | Go for explicitly configured boards |
| Listing identity | `id` is the job-post ID; `internal_job_id` is the underlying job ID; `absolute_url` is the candidate-facing URL | Post `5240259007` mapped to the Full Stack Co-op listing and its hosted application URL | Store source, board token and post ID |
| Listing timestamps | List results expose `updated_at`; individual job results expose `first_published` and `updated_at` | Selected post returned both as `2026-09-16T16:05:25-04:00`; application deadline was null | Store publication and source-update time separately from JobFlow first-seen time |
| Pagination | Official list-jobs documentation specifies no pagination parameter and returns `meta.total` | All 9 live jobs arrived in one response | Treat as an all-jobs snapshot; monitor response size and documentation changes |
| Rate/access limits | Official Job Board API documentation does not state a rate limit | Response contained no rate-limit headers | Use conservative polling, caching/backoff and record 429/5xx responses; do not claim unlimited access |
| Job content | `content=true` adds description, departments and offices | Live payload included these fields | Go; treat returned HTML as untrusted content |
| Application questions | `GET .../jobs/{id}?questions=true` is public and returns field names, types, options and `required` flags | Selected post required a transcript and three job-specific eligibility answers | Go for read-only readiness checks; unanswered required questions block readiness |
| Submit application | `POST /v1/boards/{board_token}/jobs/{id}` uses Basic Auth with the employer's Job Board API key and can create a candidate application | No key is available; POST deliberately not attempted | Blocked; no automated submission |
| Applicant validation | Form structure is job-specific; Greenhouse documents core validation while clients must render and validate the current question contract | Live form differed from generic fields and included an employer-specific file upload | Never hard-code one universal form; preserve manual handoff |

## Representative verification

### Public listing snapshot

- Board token: `aperaaiinc`
- Endpoint: `https://boards-api.greenhouse.io/v1/boards/aperaaiinc/jobs?content=true`
- Result: HTTP 200; JSON; 9 jobs.
- Observed per job: `id`, `internal_job_id`, `title`, `updated_at`,
  `location`, `absolute_url`, `language`, description content, departments and
  offices.

### Application-form inspection

- Job post ID: `5240259007`
- Listing: Software Developer - Full Stack (Co-op), Vancouver.
- Read-only endpoint used `questions=true&pay_transparency=true`.
- Core required fields: first name, last name and email.
- Employer-specific required fields: transcript file and three eligibility /
  availability questions.
- Optional fields included preferred name, phone and resume/CV on the observed
  form. Required status is job-specific and must be read rather than assumed.
- GDPR configuration was present but did not require consent for this post.
- No pay range or application deadline was exposed.

### Submission safety boundary

No POST was sent. Even an incomplete test POST is inappropriate because the
endpoint is a real external side effect and Greenhouse warns that some required
question validation is the client's responsibility. Automated tests for a
future adapter must use a fake provider; a real application requires the
user's approval of the exact destination and application package.

## Contract implications for later tickets

1. Configure an allowlist of employer board tokens; Greenhouse does not provide
   a universal cross-employer discovery feed through this endpoint.
2. Poll the all-jobs snapshot conservatively and deduplicate by
   `(source, board_token, job_post_id)`.
3. Store `first_published`, `updated_at`, `first_seen_at` and notification time
   separately so freshness claims are measurable.
4. Preserve `absolute_url` for manual handoff.
5. Fetch questions just before building or approving an application because
   employer fields can change.
6. Treat descriptions and question labels as untrusted external text.
7. Do not implement the POST adapter unless an employer supplies and authorizes
   a Job Board API key and a non-production verification path is agreed.

## Sources

- [Greenhouse Job Board API documentation](https://docs.greenhouse.io/job-board.html)
- [Greenhouse API overview](https://support.greenhouse.io/hc/en-us/articles/10568627186203-Greenhouse-API-overview)
- [Greenhouse careers-page integration options](https://support.greenhouse.io/hc/en-us/articles/200721644-Choose-a-careers-page-integration-option)
- [Apera AI public job board](https://job-boards.greenhouse.io/aperaaiinc)
- [Representative application page](https://job-boards.greenhouse.io/aperaaiinc/jobs/5240259007)

## Validation mapping

- **TC-01 passed:** official docs and the live board agreed on access method,
  IDs, fields and timestamps. Jobs-list pagination and rate limits are not
  documented, and that uncertainty is recorded rather than guessed.
- **TC-02 passed:** the real job-specific application schema was inspected via
  a public GET without submitting or sending applicant data.
- **TC-03 passed:** API submission is explicitly blocked for lack of authorized
  employer credentials; the supported decision is manual handoff.
