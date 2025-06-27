from openai import OpenAI
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Interview Bot", page_icon="💬", layout="wide")

if 'info_completion' not in st.session_state:
  st.session_state['info_completion'] = False
if 'messages' not in st.session_state:
  st.session_state['messages'] = []
if 'user_msg_count' not in st.session_state:
  st.session_state['user_msg_count'] = 0
if 'feedback_shown' not in st.session_state:
  st.session_state['feedback_shown'] = False
if 'chat_complete' not in st.session_state:
  st.session_state['chat_complete'] = False
if 'restart_requested' not in st.session_state:
  st.session_state['restart_requested'] = False
  
def complete():
  st.session_state['info_completion'] = True

def feedback_complete():
  st.session_state['feedback_shown'] = True

def restart_interview():
    keys_to_clear = [
    'info_completion', 'messages', 'user_msg_count', 'feedback_shown', 
    'chat_complete', 'feedback_content', 'name', 'experience', 'skills',
    'level', 'position', 'company', 'openai_model'
  ]
    for key in keys_to_clear:
      if key in st.session_state:
        del st.session_state[key]
      
    st.session_state['restart_requested'] = True
    st.rerun()

if st.session_state.get('restart_requested',False):
  st.session_state['restart_requested'] = False
  st.rerun()

st.title('Chat bot')
if not st.session_state['info_completion']:
  st.subheader('Personal Information', divider='rainbow')

  if 'name' not in st.session_state:
    st.session_state['name'] = ''
  if 'experience' not in st.session_state:
    st.session_state['experience'] = ''
  if 'skills' not in st.session_state:
    st.session_state['skills'] = ''
  st.session_state['name'] = st.text_input(label='Name',placeholder='Enter your name',max_chars=40, value = st.session_state['name'], )
  st.session_state['experience'] = st.text_area(label='Experience',placeholder='Enter your experience',max_chars=200,value=st.session_state['experience'],height=None)
  st.session_state['skills'] = st.text_area(label='Skills',placeholder='Enter your skills',max_chars=200,value=st.session_state['skills'],height=None)
  st.subheader('Company and Job Information', divider='rainbow')
  if 'level' not in st.session_state:
    st.session_state['level'] = 'Mid'
  if 'position' not in st.session_state:
    st.session_state['position'] = 'Data Scientist'
  if 'company' not in st.session_state:
    st.session_state['company'] = 'Google'
  col1,col2 = st.columns(2)
  with col1:
    st.session_state['level'] = st.radio(label = 'Choose level', options=['Intern','Junior','Mid','Senior'], horizontal=True,key='visibility')

  with col2:
    st.session_state['position'] = st.selectbox('Choose position',sorted(('Data Scientist','Data Engineer','Machine Learning Engineer','BI Analyst','Financial Analyst','Full Stack Developer','Software Engineer','DevOps Engineer','Cloud Engineer','AI Researcher','AI Engineer','Data Analyst','Business Intelligence Developer','Database Administrator','Systems Analyst','Network Engineer','Security Analyst','Web Developer','Mobile Developer')))

  st.session_state['company'] = st.selectbox(
    'Choose company',
    sorted(('Google', 'Microsoft', 'Amazon', 'Facebook','Nestle', 'Apple', 'Tesla', 'IBM', 'Intel', 'Oracle','accenture', 'Salesforce', 'SAP', 'Cisco', 'Adobe', 'Nvidia', 'Twitter', 'LinkedIn', 'Spotify', 'Zoom','zoho', 'Slack', 'Atlassian', 'Shopify', 'Square', 'Stripe', 'PayPal', 'eBay', 'Reddit', 'Snapchat','Pinterest', 'TikTok', 'ByteDance', 'Alibaba', 'Tencent', 'Baidu', 'Huawei', 'Xiaomi', 'JD.com','Zalando','Booking.com','Airbnb','Uber','Lyft','DoorDash','Postmates','Instacart','Robinhood','Coinbase')),
  )

  st.write(f".Your name is {st.session_state['name']} and you have {st.session_state['experience']} experience with skills {st.session_state['skills']} plus you are  {st.session_state['level']} {st.session_state['position']} at {st.session_state['company']}.")
  if st.button('Start Interview',on_click=complete):
    st.write('Starting interview...')
if st.session_state['info_completion'] and not st.session_state['chat_complete'] and not st.session_state['feedback_shown']:

  client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"], base_url=st.secrets["OPENAI_BASE_URL"])

  if 'openai_model' not in st.session_state:
    st.session_state['openai_model'] = 'gpt-4o'

  if len(st.session_state.messages) == 0:
    st.session_state['messages']= [{'role': 'system', 'content': f'''You are aan HR executive that interviews an interviewee called {st.session_state["name"]} with experience {st.session_state["experience"]} and skills {st.session_state["skills"]}.You should ask interview them for the position {st.session_state["level"]}{st.session_state["position"]} at the company{st.session_state["company"]}.Note that you only have 5 questions to ask and you should not ask any additional questions.no follow up questions are allowed. each question should be a single question and not a list of questions. Also the questions should be able answer by the interviewee with a single answer.Ask single question at a time and wait for the answer before asking the next question. Do not ask any additional questions or follow up questions. Do not ask about personal information or sensitive information. Do not ask about salary or benefits. Do not ask about the company or the position. Do not ask about the interview process or the interviewer's opinion. Do not ask about the interviewee's opinion on the company or the position. Do not ask about the interviewee's opinion on the interview process. Do not ask about the interviewee's opinion on the interviewer.'''}]

  st.markdown(
    """
    <div style="padding:10px; border-radius:8px; background-color:#f0f2f6; border:1px solid #d3d3d3; font-weight:500;
    color:black;
    font-size:16px;
    font-weight:600;">
        👋 <span>Start with a greeting</span>
    </div>
    """,
    unsafe_allow_html=True
)
  for message in st.session_state.messages:
    if message['role'] != 'system':
      with st.chat_message(message['role']):
        st.markdown(message['content'])
  if st.session_state['user_msg_count'] < 6:
    if prompt := st.chat_input('Your answer', max_chars=1000):
      st.session_state.messages.append({'role': 'user', 'content':prompt})
      with st.chat_message('user'):
        st.markdown(prompt)

      if st.session_state['user_msg_count'] < 6:
        with st.chat_message('assistant'):
          stream = client.chat.completions.create(
            model =st.session_state['openai_model'],
            messages = [
            {'role': m['role'], 'content' : m['content']} for m in st.session_state.messages
            ],
            stream=True
          )
          response = st.write_stream(stream)
        st.session_state.messages.append({'role': 'assistant', 'content': response})
        st.session_state['user_msg_count'] += 1

  if st.session_state['user_msg_count'] >=6:
    st.session_state['chat_complete'] = True
    st.write('Interview completed!')

if st.session_state['chat_complete'] and not st.session_state['feedback_shown']:
  if st.button('Get Feedback', on_click=feedback_complete):
    st.write('Fetching feedback...')

if st.session_state['feedback_shown']:
  st.subheader('Feedback')

  conversation_history = '\n'.join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])

  feedback_client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"],base_url=st.secrets["OPENAI_BASE_URL"])

  feedback_response = feedback_client.chat.completions.create(
    model = st.session_state['openai_model'],
    messages = [{'role': 'system',
       'content': """You are a helpful assistant that provides feedback on interview performance.
       Before the feedback give a score from 1 to 10.
       Follow this format:
       Overall Score: // Your score \n
       Feedback: // here put your feedback
       Give only the feedback do no ask additional questions.
       
       model:
              Feedback

        By using indexing for faster queries, sharding to distribute data across servers, and applying efficient schema design to minimize redundant or excessive data. I also optimize queries and monitor database performance regularly to address bottlenecks.

        Evaluation Feedback

        Overall Score: 7/10

        Feedback:

            You demonstrated a strong foundational understanding of the MERN stack and the ability to approach challenges creatively, as shown in your explanation of the "friends of friends" suggestion algorithm.
            Your explanation of debugging and state management, while clear, could use more depth, particularly regarding tools or advanced strategies you might use in a professional setting.
            Your answer on designing a RESTful API was straightforward, but it missed details about specific tools or methodologies, like how you might handle token management or security considerations (e.g., JWT or OAuth).
            Your explanation of MongoDB scalability strategies was well-rounded but could include more emphasis on real-world implementation challenges and monitoring tools you might rely on, like Mongoose-deployed solutions or MongoDB Atlas insights.

        Overall, your responses are solid for a junior-level position, but adding more depth and reflecting on best practices in a professional environment can greatly improve your performance. Keep practicing!
              """},
       {'role': 'user',
        'content': f'This is the interveiw you need to evaluate. Keep in mind that you are only a tool. And  you should not engage in conversation: {conversation_history}'
       }
    ]
  )

  st.write(feedback_response.choices[0].message.content)

  if st.button('Restart Interview', type ='primary',on_click = restart_interview):
    st.write('Restarting interview...')

