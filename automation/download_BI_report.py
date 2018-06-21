# -*- coding: utf-8 -*-
import logging, sys, os

sys.path.append(os.path.dirname(__file__))

from browserdriver import BrowserDriver
from requestsloader import RequestsLoader
from processagent import ProcessAgent
from utils.commands import mk_dir #trigger_send_to_ftpserver

from exceptions.exceptions import InvalidCredentials, ReportCriteriaError
from selenium.common.exceptions import NoSuchElementException

# Global Vars
from automation.config import PARMFILE_NAME, DEF_SHEET_NAME, \
                         USERNAME, PASSWORD, BASE_URL, \
                         IS_REMOTE, IS_USER_NEEDED, \
                         HOSTNAME, PORT

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    #filename='app.log',
                    filemode='w'
    )

def download_report(parameter_file=PARMFILE_NAME, host=HOSTNAME, port=PORT, is_remote=IS_REMOTE, \
                    username=USERNAME, password=PASSWORD, url=BASE_URL):
    # init the request object from excel parameter file
    try:
        logging.debug('load parameter file')
        loadrequest = RequestsLoader()
        loadrequest.load_workbook(parameter_file)
    except FileNotFoundError as e:
        logging.error(e)
        return False, 'The parameter file is not found'
    except Exception as e:
        logging.error(e)
        raise

    # get the requests from the request objects, type is list
    # the single request is a dict
    try:
        logging.debug('get request reocrds')
        requests = loadrequest.get_requests()
        receiver_email_addr = loadrequest.get_email()
    except Exception as e:
        raise

    #init process agent object
    process_agent = ProcessAgent()

    # make up the dirctory in selenium server to store the report for user
    # and return the dirctory name 
    if is_remote:
        try:
            dir_name = mk_dir(receiver_email_addr, host)
        except Exception as e:
            logging.error('error occurred in the make dir %s' %e)
            return False, 'Error occurred in the make dir'
    else:
        dir_name = ''

    # for each of request in the parameter file:
    for request in requests:
        # generate the selenium functions from the request, the funcion
        # is to be executed in selenium server
        request_functions = process_agent.makeup_functions(request)

        #init the browser driver object
        with BrowserDriver(host=host, port=port, is_remote=is_remote, \
                    username=username, password=password, url=url, \
                    dirname=dir_name) as driver:

            #loop the functions for  the request and involve browser drvier 
            # to run the functions
            for func, value in request_functions.items():
                try:
                    process_agent.process_request(driver, func, value)
                except InvalidCredentials as e:
                    return False, 'The provided credentials are invalid. \
                        Please type your credentials for authentication.'
                except ReportCriteriaError as e:
                    return False, 'The report can not run successfully,\
                        Please double check your input criteria!'
                except NoSuchElementException as e:
                    return False, 'The necessary field is invalid, please \
                    check your input or your authentication'
                except Exception as e:
                    raise
                    
    # if is_remote:
    #     try:
    #         trigger_send_to_ftpserver(host)
    #     except Exception as e:
    #         logging.error('error occurred in the send to ftpserver %s' %e)
    #         return False, 'Error occurred in the send to ftpserver'
            
    return True, 'The report run successfully'

if __name__ == '__main__':
    status, msg = download_report()
    print(status, msg)