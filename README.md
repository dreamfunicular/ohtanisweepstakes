# Ohtani Sweepstakes Site
## by Anna Hope Lynch

The Ohtani Sweepstakes (hasohtanisignedyet.com) app is an AI-powered static website that displays major MLB signing contests, including, prominently, that for Los Angeles Angels Pitcher and Designated Hitter Shohei Ohtani. The site uses a simple layout, describing whether each player has been signed yet and, if so, displaying a link to an ESPN article describing the signing and displaying an AI-generated image of that player in the uniform of the team to which they signed, at that team's ballpark. 

Every 10 minutes, or whenever traffic increases by 1000% in the span of one minute, a program on the server makes a request to the ESPN MLB API. It then scans the recent articles for any containing "Ohtani" in their headlines. If it finds an article, it will prompt the ChatGPT API whether that article confirms Ohtani's signing. If so, the program will initiate the update process.

### Workflow Process

1. Request ESPN MLB News API
2. Scan ESPN MLB News API response for posts with the name of any shortlisted player in the headline
3. For each article with the name of a shortlisted player in the headline, prompt the ChatGPT API to determine whether the article confirms each player has signed with any specific team.
4. If the ChatGPT API states that the article confirms with a team, ask it with which team that player has signed.
5. Update the static site HTML to change the player's status to SIGNED TO <TEAM> with an <a> tag linking to the appropriate article.
6. Prompt the DALL-E 2 API to generate an image of the player in the uniform of the team to which they have signed at that team's ballpark.
7. Download the generated image and replace the profile of that player with that image in the static site page.
8. Send an e-mail to the site administrator indicating the change has been made.
9. Remove the name of the player from the shortlist.
10. Return to sleep.

### License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License (AGPL) as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the [https://www.gnu.org/licenses/agpl-3.0.en.html](GNU Affero General Public License) for more details.

You can view the full license text for the GNU Affero General Public License (AGPL) at [https://www.gnu.org/licenses/agpl-3.0.en.html](https://www.gnu.org/licenses/agpl-3.0.en.html).