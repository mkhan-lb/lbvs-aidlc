# Logicbroker glossary comparison

Product vocabulary + engineering evidence · Compared 11 September 2026

[Product glossary, pinned commit 19db37c5](https://github.com/Logicbroker/product-aidlc/blob/19db37c5ea7358d751d2735c6a5260870072e633/Conventions/Glossary.md) · [Repository-derived Confluence draft, version 2](https://go.confluence.logicbroker.com/wiki/spaces/Engineerin/pages/2881126401)

Use the product glossary as the starting structure for business vocabulary and enrich it with the repository draft’s identifiers, mappings and evidence. Our draft is too implementation-focused to be the complete company glossary. Neither document should be adopted unchanged.

## How the two documents compare

| Area | Our Confluence draft | Product glossary |
| --- | --- | --- |
| Coverage | 58 term entries; API, connectors, core, data layer and queues | 100 bullet entries across 11 sections; product process, retail, logistics, business models and platform features |
| Evidence | Per-entry links to files and lines at pinned Git commits | Product conventions and two named training decks; limited per-entry provenance |
| Review state | All entries pending human verification; 10 explicitly marked interpretations | Front matter says stub; 3 product-domain placeholders; ESD and EDD only expand the acronyms |
| Reading experience | Alphabetical, detailed, editable; useful when following code | Grouped by topic, short definitions; easier to read for product and business context |
| Main weakness | Business definitions sometimes reduced to a field or class | Some broad claims mix definitions with policy, configuration or typical process |

## What the product glossary adds

| Area | Missing or thin in our draft | Treatment |
| --- | --- | --- |
| Business models | Marketplace, 1P, 3PL Fulfilled, B2B and D2C models, seller-of-record concepts, GMV and COGS | Add reviewed business meanings. Separate commercial model from fulfilment method; validate financial and contractual details with owners. |
| Product capabilities | Message Center, Self-Service Onboarding, Vendor Scorecard, Payment Center, Notification Engine, Monitoring and Advanced Analytics | Add current product definitions and owners. Confirm names, refresh schedules and behaviour before treating training descriptions as guarantees. |
| Operational vocabulary | Mixed Cart, Safety Stock, Stockout, Reverse Logistics, Packing Slip, GS1 Label, tracking, freight, 3PL, WMS, ERP, OMS and PIM | Include terms needed to read requirements and customer workflows; cross-link deeper industry detail. |
| EDI business vocabulary | 850, 855, 856, 810, 180, 846, 832; Order Change (860) and Credit Memo (812) | Add a separately labelled X12 mapping field after validation. Keep business document, syntax, transport and internal class distinct. |
| Product process | PIB, Epic, Private preview, Public preview and GA | Keep a separate product-process section or link to product conventions, so delivery vocabulary stays distinguishable from commerce workflows. |

## What our draft contributes

| Area | Examples | Treatment |
| --- | --- | --- |
| Identity and references | Logicbroker key, Link key, Source key, Destination key, Order number, Partner PO, Supplier PO, SKU and Item identifier | Retain these distinctions. They prevent agents and engineers from treating different identifiers as interchangeable. |
| Integration mechanisms | Connector, Connector name/property, API script, Custom action, OAuth connection, Map, Validation rule and Webhook | Retain code names and source links as engineering notes under clear business definitions. |
| Internal architecture | COAT, COMB, Core, Data layer, Queue message, Route/Events/Inventory/Workflow queues | Keep in a platform-internals section; avoid crowding out customer-facing terminology. |
| Explicit limits | Unresolved identifier meaning, null IsDropShip handling, transport versus format, and shipment versus delivery | Keep uncertainty visible until a domain owner settles it. A source-backed entry is not automatically an approved definition. |

## Definitions to reconcile

| Concept | Our draft | Product glossary | Review decision |
| --- | --- | --- | --- |
| [Dropship](https://github.com/Logicbroker/product-aidlc/blob/19db37c5ea7358d751d2735c6a5260870072e633/Conventions/Glossary.md#L146) | Defined through nullable IsDropShip on an order line. | Describes supplier fulfilment and the commercial execution model. | Lead with the business definition, then document the field and its nullable semantics. Do not infer financial arrangements from the flag. |
| [Company / COID / Retailer / Supplier](https://github.com/Logicbroker/product-aidlc/blob/19db37c5ea7358d751d2735c6a5260870072e633/Conventions/Glossary.md#L249) | Company/account meaning is an interpretation; sender and receiver are document roles. | COID is an account ID with an order-direction example; Retailer / Supplier remains a placeholder. | Use COID as an account-identifier entry. Define parties separately. Preserve the order example without extending its direction to every document. |
| [POC / Product Management Center](https://github.com/Logicbroker/product-aidlc/blob/19db37c5ea7358d751d2735c6a5260870072e633/Conventions/Glossary.md#L231) | POC means Product Onboarding Center; current branding is explicitly unresolved. | Product Management Center describes a marketplace product-data workflow. | Ask the product owner whether these are aliases, successive names or separate capabilities. This comparison does not establish equivalence. |
| [Product feed](https://github.com/Logicbroker/product-aidlc/blob/19db37c5ea7358d751d2735c6a5260870072e633/Conventions/Glossary.md#L208) | The entry currently describes a legacy processing arrangement and its inventory-queue path. | Describes the product-content exchange and associates it with X12 832. | Our definition is too narrow. Define the business concept first; move the legacy queue path to engineering notes and distinguish it from POC processing. |
| [Document lifecycle](https://github.com/Logicbroker/product-aidlc/blob/19db37c5ea7358d751d2735c6a5260870072e633/Conventions/Glossary.md#L193) | Describes individual contracts without asserting a universal sequence. | Adds acknowledgement, shipment, invoice and return timing; inventory-feed cadence is described as daily. | Record typical flow separately from contractual constraints. Confirm partner-specific exceptions, supported schedules and who owns refunds. |
| [Document status / Workflow](https://github.com/Logicbroker/product-aidlc/blob/19db37c5ea7358d751d2735c6a5260870072e633/Conventions/Glossary.md#L252) | StatusCode and the Statuses API; workflow queue and configured processing. | Adds status examples 0 and 1000, retailer customisation and API-driven composable workflow. | Combine default examples with explicit configuration scope. Do not present a generic state number as a full state machine or assume composable workflow equals the queue implementation. |
| [Business rules / Maps / Document Standards](https://github.com/Logicbroker/product-aidlc/blob/19db37c5ea7358d751d2735c6a5260870072e633/Conventions/Glossary.md#L259) | Separates scripted manipulation, mapping templates and simpler validation. | Business Rule Engine wording includes mapping; Document Standards describe partner compliance requirements. | Define the broad product capability and its separate implementation mechanisms. Cross-link rather than make every term an alias. |
| [Backorder / Order lines / Warehouse inventory](https://github.com/Logicbroker/product-aidlc/blob/19db37c5ea7358d751d2735c6a5260870072e633/Conventions/Glossary.md#L234) | Backorder is an acknowledgement type; Order line is a contract; Warehouse availability contains location-level quantities and future availability. | Adds the out-of-stock business condition, aggregated line-level progress, and warehouse-level inventory. | These are complementary, with different granularity. Keep line item separate from its aggregated fulfilment status. |

## Technical wording to correct or verify

### JSON and XML

The product glossary says neither has a published standard, and describes JSON as tag-based. Both have published specifications. Distinguish standard syntax from partner-specific schemas. JSON’s value/object/array model also differs from XML markup.

[RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) · [W3C XML specification](https://www.w3.org/TR/xml/)

### API delivery guarantees

Remove the generic guaranteed-delivery claim unless it points to a specific Logicbroker guarantee. HTTP has communication failures and explicit retry/idempotency semantics; using an API alone does not establish delivery guarantees.

[HTTP semantics, §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)

### API-key placement

The product glossary requires a URL query parameter. Logicbroker support documentation repeats that instruction, while official Commerce API examples use a SubscriptionKey header. Reconcile this with the API owner and document the supported mechanisms and scope; do not promote the query-only wording as a universal rule.

[Logicbroker API Authentication](https://support.logicbroker.com/kb/logicbroker/360022068791-API-Authentication) · [Commerce API documentation](https://dev.logicbroker.com/)

### Shipping limits and refresh schedules

The product glossary’s parcel and freight weight thresholds overlap, and its inventory/analytics entries specify daily updates. Treat these as contextual descriptions to verify against supported services and configuration, rather than universal definitions.



## Proposed combined entry format

1. Term and aliases
2. Business definition in one or two sentences
3. Product scope and usage/example
4. API fields / internal types / X12 mapping, where relevant
5. Sources: product documentation plus pinned implementation references
6. Owner, review status and last reviewed date

## Recommended review order

1. Resolve the unfinished party and product names, POC versus Product Management Center, and the product-feed definition first.
2. Merge business meanings with engineering evidence term by term. Preserve explicit unresolved questions.
3. Correct the technical wording and confirm configuration-dependent claims with the relevant owners.
4. Use one canonical definition per concept, with product/business and engineering views that reference it. Keep product-process terms separate.
5. Use SST-149 for the review and repository handover, and coordinate the resulting Logicbroker content with SST-146’s AIDLC integration.

This is a comparison of the two retrieved documents, with targeted checks against official specifications and API documentation. It is not a fresh audit of every implementation, training-deck claim, deployment or tenant setting. No Confluence page, Jira ticket or repository source was changed.

