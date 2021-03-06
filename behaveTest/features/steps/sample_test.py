import time

from behave import given, then, when
import behave_webdriver
from selenium.common.exceptions import NoAlertPresentException,WebDriverException
@given(u'For given user "{user_name}" ph "{phone:d}" quantity "{qty:d}"')
def sample_given(context, user_name, phone, qty):
    print('Running sample_given')

    context.user_name = user_name
    context.phone = phone
    context.qty = qty


@when('when placing order')
def sample_when(context):
    print('calling sample when')
    context.driver.find_element_by_xpath(
        '//*[@id="page-content-wrapper"]/div[2]/div/div/div[2]/div[1]/input').send_keys(context.user_name)
    context.driver.find_element_by_xpath(
        '//*[@id="page-content-wrapper"]/div[2]/div/div/div[2]/div[2]/input').send_keys(context.phone)
    context.driver.find_element_by_xpath(
        '//*[@id="page-content-wrapper"]/div[2]/div/div/div[2]/div[3]/input').send_keys(context.qty)
    context.driver.find_element_by_xpath('//*[@id="submitfrm"]').click()


@then('reciving success alert')
def sample_then(context):
    print('calling sample_then')
    time.sleep(5)
    try:
        alert = context.driver.switch_to.alert
        alert_txt = alert.text
        assert 'Success' in alert_txt, 'Found "%s" instead ' % alert_txt
        alert.accept()
    except NoAlertPresentException:
        print('NoAlertPresentException')
        context.driver.switch_to.parent_frame()
       # context.driver.manage().window().maximize()
        pass


@when('when move to admin page')
def when_admin_click(context):
    try:
        print('menu-toggle ')
        context.driver.find_element_by_xpath('//*[@id="menu-toggle"]').click()
        time.sleep(5)
        print('sidebar-wrapper ')
        context.driver.find_element_by_xpath('//*[@id="sidebar-wrapper"]/ul/li[3]/a').click()
        time.sleep(5)

    except WebDriverException:
        print('WebDriverException ')
        #context.driver.open_url('http://backend:5000/admin')

   # context.driver.find_element_by_xpath('//*[@id="grid-data"]/tbody/tr[1]/td[4]/button[1]').click()
    context.driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/div/table/tbody/tr[1]/td[4]/button[1]').click()

    time.sleep(5)




@then('check verify edit alert')
def check_edit_message(context):
    try:
        alert = context.driver.switch_to.alert
        alert_txt = alert.text
        expected_txt = "You pressed edit on row: " + str(context.phone)
        assert expected_txt in alert_txt, 'Found "%s" instead ' % alert_txt
        alert.accept()
    except NoAlertPresentException:
        print('NoAlertPresentException')
        context.driver.switch_to.parent_frame()
        #context.driver.open_url('http://backend:5000/admin')
        pass


@when('delete button click')
def when_delete_click(context):
    context.driver.find_element_by_xpath('//*[@id="grid-data"]/tbody/tr[1]/td[4]/button[2]').click()
    time.sleep(5)


@then('displaying no data found')
def no_data_found(context):
    msg_data=context.driver.get_element_text('//*[@id="grid-data"]/tbody/tr/td')
    assert 'No results found!' in msg_data, 'Found "%s" instead ' % msg_data



