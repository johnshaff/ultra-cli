"""
Text templates used throughout the Ultra CLI application.
"""

# Template for transcription formatting with exact wording
TRANSCRIBE_EXACT = """\
Give me back the text of this document formatted in paragraph form, with speaker titles if 
they are applicable and it is possible to decipher. This is from audio transcription so there 
may be misspelled words or other oddities which I'd like you to decipher and correct without 
major revisions. The output should be in plain text, no markdown etc. Be clear where you are
interjecting and where the speaker is speaking using quotation marks such as 
'Steven then said "there are a lot of problems with the economy"' etc. Your purpose is to truly
represent the transcription in a more readable format, it is NOT to summarize.

Do not include include an introduction or summary of the text, just the text itself. Also do not
use any spacing lines or other formatting, just the text itself.
"""

# Template for transcription with enhanced speaker separation
TRANSCRIBE_SPEAKERS = """\
Format this transcription with clear speaker separation. For each different speaker, create a 
new paragraph that begins with their name or identifier (e.g., "Speaker 1:", "John:", etc.) 
followed by their words. If speaker identities are unclear, use consistent labels (Speaker 1, 
Speaker 2, etc.) throughout the document. This is from audio transcription, so correct minor 
errors and oddities without changing the meaning or making major revisions.

Present the content in plain text with no markdown formatting. Do not use quotation marks 
unless they were actually spoken. Your goal is to make this transcription more readable with 
clear speaker transitions, while preserving the exact content and meaning of what was said.

Do not include an introduction, summary, or any explanatory text. Do not add extra spacing 
lines between speakers - just start each new speaker on a new line with their identifier.
"""

# Template for transcription with enhanced speaker separation and improved readability
TRANSCRIBE_SPEAKERS_V2 = """\
Format this transcription with clear speaker separation. For each different speaker, create a 
new paragraph that begins with their name or identifier (e.g., "Speaker 1:", "John:", etc.) 
followed by their words. If speaker identities are unclear, use consistent labels (Speaker 1, 
Speaker 2, etc.) throughout the document. This is from audio transcription, so correct minor 
errors and oddities without changing the meaning or making major revisions.

Present the content in plain text with no markdown formatting. Do not use quotation marks 
unless they were actually spoken. Your goal is to make this transcription more readable with 
clear speaker transitions, while preserving the exact content and meaning of what was said.

Smooth over natural language and transcription errors, including removing filler words, false 
starts, and repetitions, as shown in this example:

Original: 
Yeah I totally agree I think it'll be you know once we get the the demark count stacking up I think it's going to be a pretty v-shaped move yeah and then and and that comes next week sorry by Wednesday if it continues to count as it does and then next week should confirm a weekly nine as well so again it is opportunistically speaking incredible time yeah which is why you and I are putting together a trade list later on this week for yeah for pro macro and GMI will have a a list of what we think with best opportunities in the world are going to be. 
 Target: 
Speaker 2: Yeah, I totally agree, I think once we get the demark count stacking up it's going to be a pretty v-shaped move. If it continues to count as it does, then next week should confirm a weekly nine as well, so again, it is opportunistically speaking an incredible time- which is why you and I are putting together a trade list later on this week for pro macro and GMI, of what we think with best opportunities in the world are going to be.

Do not include an introduction, summary, or any explanatory text. Do not add extra spacing 
lines between speakers - just start each new speaker on a new line with their identifier.
"""

# Template for transcription with enhanced speaker separation, specialized terminology correction, and continuous speaker handling
TRANSCRIBE_SPEAKERS_V3 = """\
Format this transcription with clear speaker separation and advanced error correction. For each different speaker, create a 
new paragraph that begins with their name or identifier (e.g., "Speaker 1:", "John:", etc.) followed by their words. 
If speaker identities are unclear, use consistent labels (Speaker 1, Speaker 2, etc.) throughout the document.

This is from audio transcription, so special attention is needed for three types of corrections:

1. SPECIALIZED TERMINOLOGY: Correct misspelled specialized terminology, especially proper nouns, brand names, 
   technical terms, or names of people, places, or products. Use context to determine the correct spelling.
   
   Example:
   Original: "As you guys can see, that is either the end of black and white or the start of the XY era. Goomey, Scralp, 
   Natu, Weedle, Mankey, Talo. This one's backwards. What is this? Okay, we have Frogadir, an uncommon card, Cedra, 
   Rihorn, Servine."
   
   Corrected: "As you guys can see, that is either the end of Black and White or the start of the XY era. Goomy, Skrelp, 
   Natu, Weedle, Mankey, Taillow. This one's backwards. What is this? Okay, we have Frogadier, an uncommon card, Seadra, 
   Rhyhorn, Servine."

2. CONTINUOUS SPEAKER PARAGRAPHS: When the same speaker continues across multiple paragraphs, do NOT repeat the speaker 
   label. Only identify the speaker again when a different person begins speaking.
   
   Instead of:
   Speaker 1: Oh, cards are just falling out. Let's put those right down there. But yeah, Servine. Very nice Radiant 
   Collection card. Put that right there. What is this? Golduck? Very cool. Another black and white Golduck card. 
   Look at the artwork on that. That looks incredible.
   
   Speaker 1: Okay, here we go. Wismacot, another rare. And then we have a Luxio as well. Backwards card. Oh, I just 
   revealed it to Farfetch.
   
   Use this format:
   Speaker 1: Oh, cards are just falling out. Let's put those right down there. But yeah, Servine. Very nice Radiant 
   Collection card. Put that right there. What is this? Golduck? Very cool. Another black and white Golduck card. 
   Look at the artwork on that. That looks incredible.
   
   Okay, here we go. Wismacot, another rare. And then we have a Luxio as well. Backwards card. Oh, I just 
   revealed it to Farfetch.

3. NATURAL SPEECH CLEANUP: Smooth over natural language and transcription errors, including removing excessive 
   filler words, false starts, and repetitions, while preserving the meaning and personality of the speaker.

Present the content in plain text with no markdown formatting. Do not use quotation marks unless they were actually spoken. 
Your goal is to make this transcription more readable while preserving the exact content and meaning of what was said.

Do not include an introduction, summary, or any explanatory text. Do not add extra spacing lines between speakers - 
just start each new speaker on a new line with their identifier.
"""