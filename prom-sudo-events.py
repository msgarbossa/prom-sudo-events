#!/bin/env python3

import select
import prometheus_client
import time
import re
from systemd import journal

####################
# Global Variables #
####################

# Prometheus HTTP listener
prom_http_port = 9090
prom_http_addr = 'localhost'

# systemd identifier for filtering
journald_identifier = 'sudo'

# Setup metrics
c_sudo = prometheus_client.Counter('sudo', 'sudo success', ['event'])

# compile regex patterns
re_command = re.compile('COMMAND=')
re_session_opened = re.compile('session opened')
re_session_closed = re.compile('session closed')

def update_metrics(message: str) -> None:
  """
  Parse message and update Prometheus metrics
  """
  if re_command.search(message):
    c_sudo.labels('command').inc()
  elif re_session_opened.search(message):
    c_sudo.labels('session_opened').inc()
  elif re_session_closed.search(message):
    c_sudo.labels('session_closed').inc()

if __name__ == '__main__':

  # start http server on port
  prometheus_client.start_http_server(prom_http_port, addr=prom_http_addr)

  ###############################
  # Watch journald for messages #
  ###############################

  # j = journal.Reader(flags=journal.RUNTIME_ONLY)
  j = journal.Reader(flags=journal.SYSTEM)

  # Set the reader's default log level
  j.log_level(journal.LOG_INFO)
  
  # Only include entries since the current box has booted
  j.this_boot()
  j.this_machine()

  j.add_match(SYSLOG_IDENTIFIER=journald_identifier)

  # Move to the end of the journal
  j.seek_tail()

  # Discard old journal entries
  j.get_previous()

  # Create a poll object for journal entries
  p = select.poll()

  # Register the journal's file descriptor with the polling object
  journal_fd = j.fileno()
  poll_event_mask = j.get_events()
  p.register(journal_fd, poll_event_mask)

  ################################
  # Poll for new journal entries #
  ################################

  try:
    while p.poll():
      # process() returns APPEND if new entries have been added to the end of the journal
      if j.process() != journal.APPEND:
        continue

      for entry in j:
        update_metrics(entry['MESSAGE'])

  finally:
    print('prometheus exporter stopped')
