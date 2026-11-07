# City notes

Starting points for adapting the guide, checked on 2026-11-07. Rules and markets change, so verify each item before relying on it. Do not publish any of this in a guide without a current source.

## Questions for any new city

- How do people find apartments here: official sites, platforms, brokers or locators?
- Who pays a broker or locator?
- What is charged at move-in: deposit, move-in fee, application fee, first or last month?
- Which fees are mandatory each month?
- Is residential rent taxed? Are utilities included?
- What income test do landlords use?
- Which supermarkets and transit lines matter? Set these in the `nearby` config.
- Which source gives safety data by neighborhood?
- Is there a public MLS mirror or a local database with floor plans?

## New York

- The FARE Act took effect on June 11, 2025. Generally, a broker hired by the landlord cannot charge the tenant, and the landlord must give an itemized list of fees before signing. A tenant who hires their own broker pays that broker. Source: [NYC DCWP FAQ](https://home4.nyc.gov/assets/dca/downloads/pdf/about/FAQ-Broker-Fees.pdf).
- To verify: current limits on deposits and application fees, rent-stabilization status of each building, and landlords' income multiples.
- Suggested `nearby.transit`: subway and PATH. Many buildings are walk-ups or have no doorman, so add those as filters.

## Chicago

- Many landlords charge a non-refundable move-in fee in place of a security deposit, a pattern linked to the city's Residential Landlord and Tenant Ordinance. Treat it as a one-time cost. Source: [Domu](https://www.domu.com/landlord-resources/security-deposit).
- To verify: current state and city rules on fees, deposits and required lease documents, plus common amenity fees.
- Suggested `nearby.transit`: L and Metra.

## Austin

- Texas has no state individual income tax.
- Concessions were heavy in 2026, and reports put Austin among the top US markets for concession use. Compare net effective rent with asking rent. Source: [CRE Daily](https://www.credaily.com/?p=220524).
- Apartment locators are common and say the property pays them. Confirm the terms before signing.
- To verify: fee structures, utility billing, and walkability, since the walking-distance score may matter less than driving time. Adjust the weights for a car commute.
