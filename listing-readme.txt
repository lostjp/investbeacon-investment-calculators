=== InvestBeacon Investment Calculators ===
Contributors: thankaran
Tags: investment calculator, compound interest, inflation, fees, savings
Requires at least: 6.3
Tested up to: 7.1
Requires PHP: 7.4
Stable tag: 1.0.1
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html

Add compound growth, ongoing fee impact and inflation calculators with a block or shortcode. Calculations run in the browser.

== Description ==

Built by [InvestBeacon](https://investbeacon.eu/), a European investor education and broker comparison platform.

Help visitors explore what regular saving, portfolio costs and inflation can mean over time. Add one calculator or a switcher with all three views.

* Compound growth: estimated final value, total contributed, and gain or loss.
* Ongoing fees: compare the same scenario with and without a percentage-based ongoing fee. See direct charges separately from the total effect on compounding.
* Purchasing power: compare nominal value with an inflation-adjusted estimate in today's money.
* Change initial investment, monthly contribution, duration, annual gross return, ongoing fee, inflation and contribution timing.
* View a chart, an accessible annual table, and download annual figures as CSV.
* Choose from 11 display currencies. This changes the unit shown, with no exchange-rate conversion.
* Use multiple independent calculators on the same page.
* No account, API key or paid service is required.

Add the Investment Calculator block in the editor, or use:

[investbeacon_calculator]
[investbeacon_compound_interest]
[investbeacon_fee_impact]
[investbeacon_inflation]

Example with custom defaults:

[investbeacon_calculator initial="10000" monthly="300" years="25" rate="6" fee="0.2" inflation="2" currency="EUR" timing="end"]

The editor block displays an explanatory placeholder and controls for default assumptions. Open Preview or the published page for the interactive calculator.

= Privacy =

Calculations happen in the visitor's browser. The plugin does not send calculation inputs to a server, store visitor inputs, set cookies, use browser storage, include analytics, call an external API or load remote scripts, fonts or calculation data. All plugin assets are served by your WordPress site.

Default assumptions chosen by a site editor are stored in the normal WordPress page/post content. They are not visitor submissions. CSV exports are generated locally and saved only when a visitor requests a download. WordPress, your hosting provider and other plugins can have separate data practices.

The optional front-end credit link is off by default. Enable the block's credit toggle or add credit="true" if you want it. Clicking that link opens [InvestBeacon](https://investbeacon.eu/) as an ordinary website visit; calculator values are not attached to the link. There are also ordinary website/support links on the administrator help page. The calculator does not contact InvestBeacon in the background.

= Model and limitations =

Returns, ongoing fees and inflation are constant annual assumptions, converted into equivalent monthly factors. Contributions arrive at the beginning or end of each month, as selected. Values are calculated without intermediate rounding. Today’s-money values discount the future balance for accumulated inflation; contributions remain fixed in nominal terms.

This model excludes tax, dealing commissions, FX charges, cash withdrawals, contribution increases and variable returns. The ongoing fee is a percentage of the portfolio, not a flat dealing fee. Currency selection does not convert amounts.

These are illustrative estimates, not forecasts or investment advice. Actual returns vary and losses are possible. InvestBeacon and Athanasios Karantonis do not recommend any investment through this plugin.

== Installation ==

1. Upload the plugin ZIP using Plugins > Add New Plugin > Upload Plugin, or copy the investbeacon-investment-calculators directory into wp-content/plugins.
2. Activate InvestBeacon Investment Calculators.
3. Add an Investment Calculator block or a Shortcode block containing [investbeacon_calculator].
4. Preview the page. Optional default settings are available in the block sidebar.

Find shortcode examples under Tools > InvestBeacon Calculators. No setup account is required.

== Frequently Asked Questions ==

= Does it calculate actual investment returns or fetch market prices? =
No. It calculates an illustrative scenario from the assumptions entered. No live market data is used.

= Can visitors change the assumptions? =
Yes. Editor settings specify starting values; visitors can change the fields on the page. These changes are not saved by the plugin.

= Is a link to InvestBeacon required? =
No. The optional credit link is off by default and can be enabled by the site editor.

= What are the accepted input limits? =
Initial investment 0–100,000,000; monthly contribution 0–1,000,000; duration 1–60 whole years; gross annual return -50–50%; annual ongoing fee 0–10%; annual inflation -10–30%. Authored numeric defaults are clamped to these bounds and rounded to two decimals (years to a whole number). Invalid visitor input hides estimates until corrected.

= Which currencies are available? =
EUR, GBP, USD, CHF, PLN, SEK, DKK, NOK, CZK, HUF and RON. Selection changes display labels only.

= Where can I get support? =
Visit the [InvestBeacon contact page](https://investbeacon.eu/en/contact). Do not include personal financial details in public support requests.

== Changelog ==

= 1.0.1 =
* Prepare directory metadata with the verified contributor and supported Tested up to format.
* Prefix and clean up the shortcode registration variable after official Plugin Check review.

= 1.0.0 =
* Initial release with compound growth, ongoing fee impact and inflation calculators.
* Dynamic editor block, four shortcodes, responsive chart and annual table.
* Local CSV export and optional credit link, disabled by default.

== Upgrade Notice ==

= 1.0.0 =
Initial release.
