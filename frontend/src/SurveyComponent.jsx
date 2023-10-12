import React, { Component } from 'react';
import * as Survey from 'survey-react';
import 'survey-react/survey.css'; // Import the default CSS styles

class SurveyComponent extends Component {
  render() {
    // Define the survey JSON with two questions: Name and Email
    const surveyJSON = {
      questions: [
        {
          type: 'text',
          name: 'name',
          title: 'Please enter your name:',
          isRequired: true,
        },
        {
          type: 'text',
          name: 'email',
          title: 'Please enter your email address:',
          isRequired: true,
          validators: [
            {
              type: 'email',
              text: 'Please enter a valid email address',
            },
          ],
        },
      ],
    };

    return (
      <div>
        <h1>Simple Survey Example</h1>
        <Survey.Survey json={surveyJSON} />
      </div>
    );
  }
}

export default SurveyComponent;
