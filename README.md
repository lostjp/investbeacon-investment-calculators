# InvestBeacon Investment Calculators

Compound growth, ongoing fee impact and inflation calculators for WordPress. Calculations run in the visitor's browser. No API key or account is required.

Website: https://investbeacon.eu/

WordPress.org slug: `investbeacon-investment-calculators`

## Release 1.0.1

The included ZIP is the exact artifact accepted during WordPress.org review. It contains all readable plugin source and its GPL-2.0-or-later license. The manifest records its SHA-256. No private website source, visitor data or credentials are included.

Install the ZIP through WordPress → Plugins → Add New → Upload Plugin. Add the Investment Calculator block, or use `[investbeacon_calculator]`. See the bundled readme for the full set of shortcodes and assumptions.

Illustrative estimates, not investment advice. Actual returns vary and losses are possible. Public credit links are optional and off by default.

## Browser-only publication

Open Actions → Publish WordPress plugin → Run workflow on main.

- Leave Publish unchecked to validate the package and run publisher tests without using any SVN credentials or changing WordPress.org.
- For publication, add a repository Actions secret named `SVN_PASSWORD`, using the WordPress.org SVN-specific password for `thankaran`. Enter it only in GitHub's secret form. The workflow uses it only in the publication step.
- Run the workflow again with Publish checked to publish the verified artifact to the assigned WordPress.org SVN repository.

The publisher verifies the archive SHA-256, versions, paths and runtime file set. It stages trunk and tags/1.0.1, commits them together, then verifies the remote tag byte-for-byte. It refuses to replace a differing existing tag or an unexpected existing trunk. The SVN password is supplied over stdin and is not written to the SVN authentication cache.

Publication is manual. Pushes, pull requests and forks do not trigger deployment. Workflow permissions are read-only for repository contents. The official checkout action is pinned to a commit.

For future releases, update the approved archive and release.json together after testing and review. Never put credentials in a file, commit or workflow input.

## Local checks

`python3 -m unittest -v test_publish.py`

`python3 publish_wordpress.py`
