# Peril Adjusters — Airtable Schema Reference
**Base:** Claims Engine (`apptqydlALDDvUmk4`)
**Generated:** 2026-03-31 (live API pull)

---

## Claim Timeline
**Table ID:** `tblYpOpSDzq3HaGTt`

| # | Field ID | Field Name | Type | Options / Notes |
|---|---|---|---|---|
| 1 | `fld8nJxMwfEkQYXfi` | Title | `singleLineText` |  |
| 2 | `fldo7cBYBi1shsiCG` | Log ID | `autoNumber` |  |
| 3 | `fldNxHSebZhvgHMjr` | Date/Time | `createdTime` |  |
| 4 | `fld6zmVUasxulWus4` | Action Type | `singleSelect` | Email, Document, System, AI Task |
| 5 | `fldGRrjDpqlLUEamQ` | Description | `multilineText` |  |
| 6 | `fldb0h0MgDJLhCoyT` | Linked Claim | `multipleRecordLinks` | → `tblHX7pn8tKQdXv3X` |

## Claims
**Table ID:** `tblHX7pn8tKQdXv3X`

| # | Field ID | Field Name | Type | Options / Notes |
|---|---|---|---|---|
| 1 | `fldIZTxAJ9QmyY0z4` | Claim ID | `singleLineText` |  |
| 2 | `fldb8ZOamM2BMNeEi` | Status | `singleSelect` | Lead, Waiting on Customer Documentation, Documentation Received, Send Contract, Contract Sent, Contract Signed, Claim Needs Filed, Claim Filed, LOR Submitted, Carrier Documentation Received, Estimate Needs Completed, Estimate Submitted, Re-inspection Needs Scheduled, Re-inspection Scheduled, Engineer Appointment Needs Scheduled ... +23 more |
| 3 | `fld3CAC49jdt2EyYj` | Insurance Carrier | `multipleRecordLinks` | → `tbl6XMSCu0dMQBA9U` |
| 4 | `fldIbXWUYjCyBehvv` | Date of Loss | `date` | local |
| 5 | `fldgcyE3bI7JUKOaB` | Sub-Category | `singleSelect` | Needs Contacted - Admin, PA Review - PA, Invoice Policyholder - Admin, Submit Rebuild Invoices - PA, Collect Google Review - Admin, Hail, Fire, Water / Flood, Wind, Wind / Hail |
| 6 | `fldY8MjUAhP95NZH5` | Business / Organization Name | `singleLineText` |  |
| 7 | `fld2FjV10cS0a06hc` | Contact Full Name | `singleLineText` |  |
| 8 | `fldHopaw5fA8462sy` | Contact Phone Number | `phoneNumber` |  |
| 9 | `fldWliA1jdWXqYaUq` | Loss Address | `singleLineText` |  |
| 10 | `fldzZd2eThxQIJPDg` | Loss City | `singleLineText` |  |
| 11 | `fldapVBI9uQUvJDog` | Loss State | `singleSelect` | Texas, Missouri, Oklahoma, Ohio, Iowa, Alabama, Arkansas, Colorado, Florida, Georgia, Illinois, Indiana, Kansas, Kentucky, Louisiana ... +16 more |
| 12 | `fldmuudjqlSPwJH5a` | Loss Zip Code | `singleLineText` |  |
| 13 | `fld9Qvbn6uwFxVgnp` | Insurance Policy Number | `singleLineText` |  |
| 14 | `fldEMP9RzQCjueqJR` | Insurance Claim Number | `singleLineText` |  |
| 15 | `fldqUkokn8I2F2lC8` | Insurance Adjuster | `singleLineText` |  |
| 16 | `fldqBoSEzWmCXAenq` | Insurance Adjuster Phone | `singleLineText` |  |
| 17 | `fldGIRzfeTacK2lBB` | Insurance Adjuster Email | `email` |  |
| 18 | `fld7HAtm7YDsELNlA` | Current RCV Amount | `currency` | $ precision=2 |
| 19 | `fldmLDkA21zdrirtT` | PA Current Estimate Amount | `currency` | $ precision=2 |
| 20 | `fldvpQ3KEyiizk9aW` | Statute of Limitations | `date` | local |
| 21 | `fldIFHMcUi8EJitOv` | Proof of Loss Satisfied | `singleSelect` | Yes, No |
| 22 | `fldD1Jzb8MisOkiBA` | Proof of Loss Due Date | `date` | local |
| 23 | `fldSsphX1IfxGoWHN` | Deductible Amount | `currency` | $ precision=2 |
| 24 | `fld3Uzk5lI3ZaGbqX` | Carrier Checks Received | `multipleRecordLinks` | → `tblKBGLPeStiQbnSG` |
| 25 | `fldkqoCmizgxSDgQF` | Policyholder Payments Received | `multipleRecordLinks` | → `tblKBGLPeStiQbnSG` |
| 26 | `fldlDXrDx9iLsKDyk` | Staff Notes | `richText` |  |
| 27 | `fld6cc5wLMvIDqRTD` | Drive Folder | `url` |  |
| 28 | `fldCuRtzzOAdV6Rhf` | Last Modified | `lastModifiedTime` |  |
| 29 | `fldejJos5SI1oPPtM` | The Delta | `formula` |  |
| 30 | `fldwJn4FzSCyMhEd2` | Last Activity Date | `rollup` | field: fldNxHSebZhvgHMjr via fldfGAnxmf6PATfP0 |
| 31 | `fldlR3crf1pQRA8RD` | Days Idle | `formula` |  |
| 32 | `fldgozC5WCowmtkSQ` | SLA Flag | `formula` |  |
| 33 | `fldBHdPHNlGyq1n0H` | Invoice Amount (10% Fee) | `formula` |  |
| 34 | `fldvwoHd5g1FHM8qj` | CLUE Report Due Date | `formula` |  |
| 35 | `flda0jOOLm6Oj7MrV` | Loss Run Due Date | `formula` |  |
| 36 | `fldMz33HbvduIoJbw` | Property Address | `singleLineText` |  |
| 37 | `fldmoTetAVJP0JtYa` | Property Type | `singleSelect` | Multifamily, Church/Religious, HOA, Commercial, Large Residential, School/Nonprofit, Other |
| 38 | `fldDdoV2Bv6yhHpGK` | Estimated Claim Amount | `currency` | $ precision=0 |
| 39 | `fldJNPJpNhLrSfCQ5` | Insured Name | `singleLineText` |  |
| 40 | `flddxWq39e1oYoic4` | Insured Email | `email` |  |
| 41 | `fldOv5Z141ErKNS3k` | Insured Phone | `phoneNumber` |  |
| 42 | `fldjpyCrWTJ9SlYj1` | Contact | `multipleRecordLinks` | → `tbloPiICnA4GxSIXi` |
| 43 | `fldEVLFUhUHDcMepv` | Policy Number | `singleLineText` |  |
| 44 | `fldRSXyEPrl5Y60Lr` | Loss Type | `singleSelect` | Hail, Wind, Fire, Water, Hurricane, Storm, Roof, Structural, Multi-Peril, Other, co, Collapse, Tornado |
| 45 | `fldT4ntpKYgV39Ejn` | Date of Representation | `date` | local |
| 46 | `fld9AQo0DkcPbZoyx` | Filed with Carrier | `checkbox` |  |
| 47 | `fldwhxaJMIHssSEOj` | Confirmed Damage | `checkbox` |  |
| 48 | `fld7Airl4LrDQ1DKs` | Lead Source | `singleSelect` | Contractor Referral, Website, AI Chat, Storm Outreach, Fire Dispatch, News Monitoring, Direct Mail, Word of Mouth, Google Ads, LinkedIn, Repeat Client, Lead Purchase, @PartnerBot SMS, HailTrace |
| 49 | `flddV5Mp96bmS1fMd` | Lead Source Detail | `singleLineText` |  |
| 50 | `fldQqQwT9HUQLbOV9` | Contractor (Referral) | `multipleRecordLinks` | → `tblq6TFvKXx9PfhQm` |
| 51 | `fldiTXcbH5Kn8CURn` | Approved By | `singleLineText` |  |
| 52 | `fldthZLExnTekPpBy` | Approved Date | `date` | local |
| 53 | `fldPFRDdJmPhPrwld` | State | `singleSelect` | Texas, Missouri, Oklahoma, Ohio, Iowa, Alabama, Arkansas, Colorado, Florida, Georgia, Illinois, Indiana, Kansas, Kentucky, Louisiana ... +15 more |
| 54 | `fldozsktEJJjHFJbl` | Contract Status | `singleSelect` | Not Sent, Sent, Signed, Expired |
| 55 | `fldlbCeyR9MOSAtCA` | Contract Sent Date | `date` | local |
| 56 | `fldXYBSuAsC1id308` | Contract Signed Date | `date` | local |
| 57 | `fldyyPwOX2jgrS1il` | DocuSign Envelope ID | `singleLineText` |  |
| 58 | `fldrneWj87CGdaubJ` | LOR Sent Date | `date` | local |
| 59 | `fldoUwa1NpRNbXZqX` | Carrier Response | `singleSelect` | Acknowledged, Adjuster Assigned, Inspection Scheduled, Payment Issued, Underpaid, Partial Denial, Full Denial, Reservation of Rights, No Response, Awaiting Supplemental, Awaiting Depreciation Invoices |
| 60 | `fldmZqVsPXgz3bd8W` | Carrier Adjuster | `multipleRecordLinks` | → `tbl3MsKPn5UQ2xPj5` |
| 61 | `fld69x0BKneqqmHkO` | Inspector | `singleLineText` |  |
| 62 | `fldyQagEJHtYTMwGW` | Appraiser (Peril) | `singleLineText` |  |
| 63 | `fldmVsK0p5cY5abq9` | Appraiser (Carrier) | `singleLineText` |  |
| 64 | `fldFfD4efiXGiQUII` | Umpire | `singleLineText` |  |
| 65 | `fld4fZxO6GGo2IMXc` | Engineer | `singleLineText` |  |
| 66 | `fldgvjAy1JYTFYgK6` | Inspection Status | `singleSelect` | Not Scheduled, Scheduled, Complete, Joint Pending |
| 67 | `flduR3GYRj1TPxhjb` | Inspection Date | `date` | local |
| 68 | `fld4hb6hZYLacGXQS` | Xactimate Estimate | `currency` | $ precision=2 |
| 69 | `fldqmNquYiuWNLasc` | Carrier Initial Offer | `currency` | $ precision=2 |
| 70 | `fldG4p1VOAo16FS9F` | Carrier Revised Offer | `currency` | $ precision=2 |
| 71 | `fldZ0Q35dJijfbgda` | Final Settlement | `currency` | $ precision=2 |
| 72 | `fldx6uE5ZV00e1a3U` | Fee % | `percent` |  |
| 73 | `fldGTDjwwowJzGNuM` | ACV Received | `currency` | $ precision=2 |
| 74 | `fldPHXQckJTfVOFX4` | Depreciation Held | `currency` | $ precision=2 |
| 75 | `fld9hrOo2jhrU82Fa` | Depreciation Released | `currency` | $ precision=2 |
| 76 | `fldHsvelrCS9KaK2n` | Depreciation Status | `singleSelect` | N/A, Pending Repairs, Reminded 30d, Reminded 60d, Reminded 90d, Recovered, Stalled, Waived |
| 77 | `flduLE7ZaSPJJHczf` | Supplement Round | `number` |  |
| 78 | `fldcgmhlZQ1OWtEmF` | Supplement Amount | `currency` | $ precision=2 |
| 79 | `fldbWntXSgs3d7iqv` | Escalation Type | `singleSelect` | None, Appraisal, Attorney, Demand Letter, DOI Complaint |
| 80 | `fldx80QfJahSCx0YD` | Attorney | `multipleRecordLinks` | → `tbl4ve4i5tm67y7dt` |
| 81 | `fldYqlHGMXqKgCUdV` | Appraisal Status | `singleSelect` | N/A, Invoked, Appraiser Selected, Umpire Needed, Award Issued |
| 82 | `fldW86gKy0CVkJVDu` | Appraisal Award | `currency` | $ precision=2 |
| 83 | `fldgigxknAitS3gdb` | QBO Customer ID | `singleLineText` |  |
| 84 | `fld4iSzNL2TQjtlhG` | QBO Invoice ID | `singleLineText` |  |
| 85 | `fldwEo3dX32xomGo5` | QBO Sync Status | `singleSelect` | Synced, Pending, Error |
| 86 | `fldzsf7TWMlwN5wTd` | Brelly Status | `singleSelect` | Not Started, Policy Uploaded, Coverage Summary, Discrepancy Report, Rebuttal Generated, Settlement Audit, Complete |
| 87 | `fldwuYsv9kY0aO2qo` | Brelly Coverage Summary | `richText` |  |
| 88 | `fldjzASxAlSniosve` | CompanyCam Project ID | `singleLineText` |  |
| 89 | `fldItwoVyNep6KfaA` | Drive Folder URL | `url` |  |
| 90 | `fld31NEj1xviqaoYQ` | MyCase ID | `singleLineText` |  |
| 91 | `fldckWZmzxR61763r` | Team Notes | `richText` |  |
| 92 | `fldwEP8Ea4EYnUnLv` | Partner Queries | `multipleRecordLinks` | → `tblAOwqfAJOVfREA0` |
| 93 | `fldKVfFyNTZ3haZrW` | Partner Queries | `multipleRecordLinks` | → `tblAOwqfAJOVfREA0` |
| 94 | `fldzSYOLc8o3pVPeL` | Documents | `multipleRecordLinks` | → `tblUymYfV6WR50kOr` |
| 95 | `fldIG6yiRJ4VKPmSG` | Payments | `multipleRecordLinks` | → `tblKBGLPeStiQbnSG` |
| 96 | `fldXvf04rJCMryihU` | Statutory Deadlines | `multipleRecordLinks` | → `tblvhgCwdKV03Q1Dz` |
| 97 | `fldTwAzblgkif9kJ8` | Client Communications | `multipleRecordLinks` | → `tbl9mcbjvuPIATEuR` |
| 98 | `fldoMR0Id2fzNjJrg` | Lead Sales | `multipleRecordLinks` | → `tblUUJKhXTjyriHpO` |
| 99 | `fldSntOc96efKmBnI` | Claims Performance | `multipleRecordLinks` | → `tblHCZhICM6ykcY9s` |
| 100 | `fldLSFmmECRaFIwYe` | Uplift %  | `formula` |  |
| 101 | `fldiRoIgebZG21HBV` | Uplift Amount | `formula` |  |
| 102 | `fldDI1qpb3qZwIqtC` | Fee Amount | `formula` |  |
| 103 | `fldFeBbvFWyQEXbeU` | Days Open | `formula` |  |
| 104 | `fldfIZxRJpkMFf4BI` | Travel & Logistics | `multipleRecordLinks` | → `tbl4sWi4YiXdw0hgf` |
| 105 | `flds1bjDn1bkIuCWR` | Partner Queries 2 | `multipleRecordLinks` | → `tblAOwqfAJOVfREA0` |
| 106 | `fldrjNHIW2ICUmVlY` | Drive Folder ID | `singleLineText` |  |
| 107 | `fldIXoou8tQzz4oN2` | Docs Subfolder ID | `singleLineText` |  |
| 108 | `fld3WbSDUqaf44xje` | Photos Subfolder ID | `singleLineText` |  |
| 109 | `fldP6TxBjDaCdsK9l` | Estimates Subfolder ID | `singleLineText` |  |
| 110 | `fldkbsBODsnHWys5i` | Policy Documents | `multipleAttachments` |  |
| 111 | `fld1IJNXleOMePySw` | Carrier Estimate | `multipleAttachments` |  |
| 112 | `fldEJ9QmRcWzRojg8` | Extracted Text | `richText` |  |
| 113 | `fld7F6QC61XYSS5NK` | AI Supplement | `richText` |  |
| 114 | `fldHl1lraEJMl7Fwm` | Payment Events | `multipleRecordLinks` | → `tblkT8rKNVdK6yNWK` |
| 115 | `fldGbXRAzv0A1oTug` | Master Drive Folder | `url` |  |
| 116 | `fldzj7wbmfpJhsDJx` | Created Time | `createdTime` |  |
| 117 | `fldk3C05E6SAXjjeh` | Peril Estimate | `currency` | $ precision=2 |
| 118 | `fld1kmLHGipW2V4SE` | Approved Amount | `currency` | $ precision=2 |
| 119 | `fldpqvhJqQ84cCme1` | Paid Amount | `currency` | $ precision=2 |
| 120 | `fldxQp7SoarTpug8p` | Master Directory | `multipleRecordLinks` | → `tbllkQMU1hFoWvGGv` |
| 121 | `fldfGAnxmf6PATfP0` | Claim Timeline | `multipleRecordLinks` | → `tblYpOpSDzq3HaGTt` |
| 122 | `fld1HNqxMHWIZNcNk` | Audit Status | `singleSelect` | Pending Intake, Forensic Review, Converted to Active, Unviable |
| 123 | `fldhyQEAId3qZnfMq` | Assigned To | `singleSelect` | Trisha, Jerad, Hank |
| 124 | `fldBmXhXet3EhYWd9` | CLUE Auth Signed | `checkbox` |  |
| 125 | `fld6upXOej7k5F3AN` | Loss Run Requested Date | `date` | local |
| 126 | `fld36yvK1moXWWTbC` | Loss Run Received Date | `date` | local |
| 127 | `fldexwLJZz05uuxW9` | CompanyCam Link | `url` |  |
| 128 | `fldsbZzMJ7T5BUp8Q` | Loss Run Status | `singleSelect` | Requested, Received, Overdue |
| 129 | `fldl54l7aopla5U0u` | Recovery Attribution | `multipleSelects` |  |
| 130 | `fldGzaQq6O474fevS` | POSE Validation Score | `number` | precision=1 |
| 131 | `fldZeduHnZtP7nUz7` | Proof of Loss Deadline | `date` | local |
| 132 | `fldCrKLF6OI3Tjqyl` | Notice of Claim Deadline | `date` | local |
| 133 | `fldp9ZtxJ0Id5fw9U` | Regulatory Firewall: Peril Group Brokered | `checkbox` |  |
| 134 | `fldTUTDYJGmZadF6U` | POSE Score | `number` |  |
| 135 | `fldRDXsNK2IMqpEhR` | CLUE Requested Date | `date` | us |
| 136 | `fldHWCb6E9Vp5Hdgn` | CLUE Status | `singleSelect` | Pending, Received, Escalated |
| 137 | `fldNHBa33KtvA2rJL` | Affiliated Business Disclosure Signed | `checkbox` |  |
| 138 | `fld0corGnD4hKZyO1` | Forensic Knowledge Base | `multipleRecordLinks` | → `tbl04wLMNmfq0xPoz` |
| 139 | `fldPBhxnFUNe1Swvv` | Custom Fee % | `number` | precision=1 |
| 140 | `fldyoufDZBM8jX4aM` | Fee Override Justification | `multilineText` |  |
| 141 | `fldBsfsbn4tWP22y3` | Carrier Last Contact Date | `date` | us |
| 142 | `fldP4BlnJOwS77B3U` | ABA Disclosure Signed | `checkbox` |  |
| 143 | `fldP80mLFRnKS373h` | SLA Status | `formula` |  |
| 144 | `fldXTeSMLJJ6BHqVM` | Custom Fee Terms | `multilineText` |  |
| 145 | `fldQihUnNZo88M9nX` | Additional Property Locations | `multilineText` |  |
| 146 | `fldZ5vpPkgjKvDT2R` | Status Last Changed | `lastModifiedTime` |  |
| 147 | `fldQToBytYsrm0ULL` | Signed Disclosure Document | `multipleAttachments` |  |
| 148 | `fldT3ZIIt4ExQLhGf` | Review Sent | `checkbox` |  |
| 149 | `fldgD43scPJx5rgB6` | Master Task Tracker | `multipleRecordLinks` | → `tblcXxFOcWIpCyV7B` |
| 150 | `fldFIZugoWhGQed24` | The Vault | `multipleRecordLinks` | → `tblER7W0z6rmMDBSB` |
| 151 | `fldgENSywgt8LSGO4` | Apex Knowledge Vault | `multipleRecordLinks` | → `tblKhUXhFoiaSFhRx` |
| 152 | `fldfMkBEeOmpFlIP4` | Carrier Xactimate | `multipleAttachments` |  |
| 153 | `flddbAMPqYTQVRrth` | Peril Xactimate | `multipleAttachments` |  |
| 154 | `fld9xYGrDkoUW43hF` | Estimate Discrepancy Report | `richText` |  |
| 155 | `fldn35iSAfJqKtKnO` | Generate Contract | `button` |  |
| 156 | `fldPO3b4HCeb0Qxzg` | Contractor Email (Lookup) | `multipleLookupValues` |  |
| 157 | `fldO4INtI1fSmZnUE` | Carrier Name | `multipleLookupValues` |  |
| 158 | `fld24MI0edSqrTxCB` | PPA Notice Sent | `checkbox` |  |
