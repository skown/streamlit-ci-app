import streamlit as st
import pandas as pd
from causalimpact import CausalImpact
import searchconsole
import matplotlib.pyplot as plt
import datetime

st.title("SEO Impact Checker")

st.sidebar.write('**GSC Performance Time Period Picker**')
today = datetime.date.today()
tomorrow = today - datetime.timedelta(days=2)
start_date = st.sidebar.date_input('Start date', today)
end_date = st.sidebar.date_input('End date', tomorrow)
if start_date < end_date:
    st.sidebar.success('Start date: `%s`\n\nEnd date: `%s`' % (start_date, end_date))
else:
    st.sidebar.error('Error: End date must fall after start date.')

property_checkbox = st.checkbox('Different domains for control and experimental URLs?')
st.write(property_checkbox)

st.subheader("Put your Links")
text_control = st.text_area('Control URLs')
lines_control = text_control.split('\n')
st.write("Number of links that you want to process:", len(lines_control))
if len(lines_control) > 1000:
    st.warning(f"Maximum number of lines reached. Only the first {1000} will be processed.")
    lines_control = lines_control[:1000]

text_exp = st.text_area('Experimental URLs')
lines_exp = text_exp.split('\n')
st.write("Number of links that you want to process:", len(lines_exp))
if len(lines_exp) > 1000:
    st.warning(f"Maximum number of lines reached. Only the first {1000} will be processed.")
    lines_exp = lines_exp[:1000]

st.sidebar.subheader("Property, Metrics, Time Picker")
#Make choose which account property we want to use
if property_checkbox == False:
	gsc_property = st.sidebar.selectbox("Which Property You Want to Check?",['https://brainly.pl/','https://brainly.com/','https://brainly.in/','https://brainly.co.id/','https://brainly.com.br/','https://brainly.lat/','https://brainly.ph/','https://brainly.ro/','https://eodev.com/','https://nosdevoirs.fr/','https://znanija.com/'])
else:
	gsc_property = st.sidebar.selectbox("Which Property You Want to Check?",['https://brainly.pl/','https://brainly.com/','https://brainly.in/','https://brainly.co.id/','https://brainly.com.br/','https://brainly.lat/','https://brainly.ph/','https://brainly.ro/','https://eodev.com/','https://nosdevoirs.fr/','https://znanija.com/'])
	gsc_property_exp = st.sidebar.selectbox("Other Property to Check",['https://brainly.pl/','https://brainly.com/','https://brainly.in/','https://brainly.co.id/','https://brainly.com.br/','https://brainly.lat/','https://brainly.ph/','https://brainly.ro/','https://eodev.com/','https://nosdevoirs.fr/','https://znanija.com/'])

account = searchconsole.authenticate(client_config='client_secrets.json',credentials='credentials.json')
if property_checkbox == False:
	webproperty = account[gsc_property]
	df_control = []
	for url_control in lines_control:
		df_control.append(webproperty.query.range(start_date, end_date).dimension('date').filter('page', url_control).filter('device','DESKTOP').get())
	df_exp = []
	for url_exp in lines_exp:
		df_exp.append(webproperty.query.range(start_date, end_date).dimension('date').filter('page', url_exp).filter('device','DESKTOP').get())
else:
	webproperty = account[gsc_property]
	df_control = []
	for url_control in lines_control:
		df_control.append(webproperty.query.range(start_date, end_date).dimension('date').filter('page', url_control).get())
	webproperty_exp = account[gsc_property_exp]
	df_exp = []
	for url_exp in lines_exp:
		df_exp.append(webproperty_exp.query.range(start_date, end_date).dimension('date').filter('page', url_exp).get())		


control_frame = pd.DataFrame(columns=['Date', 'Clicks', 'Impressions', 'CTR', 'Avg_pos'])
for url in range(len(lines_control)):
	for values in df_control[url]:
		control_frame = control_frame.append({
			'Date': values[0],
			'Clicks': values[1],
			'Impressions': values[2],
			'CTR': values[3],
			'Avg_pos': values[4]
			},ignore_index=True)

exp_frame = pd.DataFrame(columns=['Date', 'Clicks', 'Impressions', 'CTR', 'Avg_pos'])
for url in range(len(lines_exp)):
	for values_exp in df_exp[url]:
		exp_frame = exp_frame.append({
			'Date': values_exp[0],
			'Clicks': values_exp[1],
			'Impressions': values_exp[2],
			'CTR': values_exp[3],
			'Avg_pos': values_exp[4]
			},ignore_index=True)

#Make choose which column we want to process
which_column = st.sidebar.selectbox("Which Metrics you want to check?",["CTR","Avg_pos"])


#ctr_control_frame = control_frame.groupby('Date')[which_column].mean().to_frame()
#ctr_exp_frame = exp_frame.groupby('Date')[which_column].mean().to_frame()
ctr_control_frame = pd.to_numeric(control_frame[which_column]).groupby(control_frame['Date']).mean().to_frame()
ctr_exp_frame = pd.to_numeric(exp_frame[which_column]).groupby(exp_frame['Date']).mean().to_frame()

results = pd.merge(ctr_control_frame, ctr_exp_frame, on='Date')
#results

st.sidebar.write('When the change started?')
test_date = st.sidebar.date_input('Test date')
st.sidebar.write('Start date:', test_date)

pre_period = [str(start_date), str(test_date-datetime.timedelta(days=1))]
post_period = [str(test_date), str(end_date)]
st.sidebar.write("Pre period:",pre_period[0] ,"-", pre_period[1])
st.sidebar.write("Post period:",post_period[0] ,"-", post_period[1])

results_corr = results.loc[results.index < str(test_date)]
url_correlation = results_corr.iloc[:,0].corr(results_corr.iloc[:,1])
#st.write(results_corr.iloc[:,0])
#st.write(results_corr.iloc[:,1])
st.write("_URL Correlation to check if groups are similar:_", url_correlation)
if url_correlation > 0.75:
	st.write("You can based on this groups")
else:
	st.write("**WARNING!** Change the control group")

ci = CausalImpact(results, pre_period, post_period)
#ci.plot()
st.subheader("""Causal Impact Chart""")
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot(ci.plot())
st.write("""*Report Summary*""")
st.write(ci.summary(output='report'))