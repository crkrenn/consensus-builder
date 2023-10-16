import React, { Component } from 'react';
import * as Survey from 'survey-react';
import 'survey-react/survey.css'; // Import the default CSS styles

class SurveyComponent extends Component {
  render() {
    // Define the survey JSON with two questions: Name and Email
    const surveyJSON = (
{
    "showQuestionNumbers": false,
    "pages": [
        {
            "name": "new_statements",
            "title": "Are your perspectives or experiences missing from the conversation? If so, add them in the box below.",
            "elements": [
                {
                    "type": "html",
                    "html": "<p>What makes a good statement?</p>\n<ul>\n  <li>Stand alone idea</li>\n  <li>Raise new perspectives, experiences, or issues</li>\n  <li>Clear & concise (limited to 280 characters each)</li>\n</ul>\n<p>A few examples:</p>\n<ul>\n  <li>Any adult should be able to buy an assault weapon</li>\n  <li>Restrictions on assault weapon ownership will harm the gun industry and lead to job losses</li>\n  <li>Every person owning or using an assault weapon should carry a license or a permit</li>\n</ul>\n"
                },
                {
                    "type": "comment",
                    "name": "statements",
                    "title": "Please remember, statements are displayed randomly, and you are not replying directly to other participants' statements. Please separate multiple statements with a period ('.').",
                    "maxLength": 2000,
                    "rows": 4
                }
            ]
        },
        {
            "name": "topics",
            "title": "Here are a few topics we're thinking about discussing next:",
            "elements": [
                {
                    "type": "checkbox",
                    "name": "topics_checkbox",
                    "title": "Which of these topics are most important to you?",
                    "colCount": 1,
                    "choices": [
                        "Giving a helping hand to groups of people who need it",
                        "Help for people who are having a hard time making ends meet",
                        "How much money the government takes from our paychecks",
                        "Keeping an eye on big companies who run the internet",
                        "Learning and schools",
                        "Making rules about how money can be used during elections",
                        "Making sure everyone has the same rights and chances to succeed",
                        "Rules about who can come and live in our country",
                        "Taking care of our planet",
                        "Women being able to choose if and when they want to have babies"
                    ]
                },
                {
                    "type": "comment",
                    "name": "topics_text",
                    "title": "Please suggest anything you think should be added. Please separate multiple topics with a period ('.').",
                    "maxLength": 2000,
                    "rows": 4
                }
            ]
        },
        {
            "name": "demographics",
            "title": "Please answer the following questions about yourself",
            "description": "We'd really appreciate it if you could answer a few questions\nabout yourself. It makes sure\nthat the opinions of a few people do not control the results.\nWe want to know what everyone thinks, not just a few people. Thank you!",
            "elements": [
                {
                    "type": "text",
                    "name": "emailAddress",
                    "title": "What is your email address?",
                    "description": "Can we have your email? We want to work on more topics like\nthis and tell Congress what most people think. Don't worry,\nwe won't give your email to anyone unless you say it's okay.",
                    "validators": [
                        {
                            "type": "email",
                            "text": "Please enter a valid email address or leave this field blank"
                        }
                    ]
                },
                {
                    "type": "text",
                    "name": "firstName",
                    "title": "What is your first name?",
                    "description": "We want to address you by name\nrather than a generic email greeting."
                },
                {
                    "type": "text",
                    "name": "lastName",
                    "title": "What is your last name?",
                    "description": "Having your full name will help us help you\ncommunicate with Congress, as well as let us know if we've had the\npleasure of meeting before."
                },
                {
                    "type": "radiogroup",
                    "name": "personalGunOwnership",
                    "title": "Do you currently own a gun?",
                    "choices": [
                        "A. Yes",
                        "B. No"
                    ]
                },
                {
                    "type": "radiogroup",
                    "name": "householdGunOwnership",
                    "title": "Do any individuals you live with currently own a gun?",
                    "choices": [
                        "A. Yes",
                        "B. No"
                    ]
                },
                {
                    "type": "radiogroup",
                    "name": "politicalAffiliation",
                    "title": "In politics today, do you consider yourself a Republican, Democrat, an independent or something else?",
                    "choices": [
                        "Republican",
                        "Democrat",
                        "Independent",
                        "Something else"
                    ]
                },
                {
                    "type": "radiogroup",
                    "name": "politicalAffiliationLean",
                    "visibleIf": "{politicalAffiliation} = 'Independent' or {politicalAffiliation} = 'Something else'",
                    "title": "As of today, do you lean more to the Republican Party or more to the Democratic Party?",
                    "choices": [
                        "Republican Party",
                        "Democratic Party"
                    ]
                },
                {
                    "type": "text",
                    "name": "zipCode",
                    "title": "What is your zip code?",
                    "validators": [
                        {
                            "type": "regex",
                            "text": "Please enter a valid 5 digit US zip code or leave this field blank",
                            "regex": "^[0-9]{5}$"
                        }
                    ]
                },
                {
                    "type": "radiogroup",
                    "name": "ageRange",
                    "title": "What age range do you fall into? Please select the option that corresponds to your current age range.",
                    "choices": [
                        "A. Under 18 years old",
                        "B. 18-24 years old",
                        "C. 25-34 years old",
                        "D. 35-44 years old",
                        "E. 45-54 years old",
                        "F. 55-64 years old",
                        "G. 65 years and older"
                    ]
                },
                {
                    "type": "radiogroup",
                    "name": "educationLevel",
                    "title": "What is your highest level of completed education? Please select the option that best describes your educational background.",
                    "choices": [
                        "A. No formal education",
                        "B. Some high school",
                        "C. High school graduate or equivalent (e.g., GED)",
                        "D. Some college or vocational training",
                        "E. Associate's degree (e.g., AA, AS)",
                        "F. Bachelor's degree (e.g., BA, BS)",
                        "G. Postgraduate or professional degree (e.g., MA, MS, PhD, MD, JD)"
                    ]
                },
                {
                    "type": "radiogroup",
                    "name": "sexAtBirth",
                    "title": "Were you born male or female?",
                    "choices": [
                        "A. Male",
                        "B. Female"
                    ]
                },
                {
                    "type": "radiogroup",
                    "name": "genderIdentity",
                    "title": "Do you describe yourself as a man, a woman, or in some other way?",
                    "choices": [
                        "A. Man",
                        "B. Woman",
                        "C. In some other way"
                    ]
                }
            ]
        }
    ]
}
);

    return (
      <div>
        <Survey.Survey json={surveyJSON} />
      </div>
    );
  }
}

export default SurveyComponent;

