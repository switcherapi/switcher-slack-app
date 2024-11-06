from controller.home import on_change_request_opened, on_home_opened
from controller.change_request import (
    on_domain_selected,
    on_environment_selected,
    on_group_selected,
    on_switcher_selected,
    on_change_request_review,
    on_submit,
    on_change_request_abort,
    on_request_approved,
    on_request_denied
)

class RequestChangeEventHandler:
    def register_events(self, app):
        """ Register events for the Request Change feature """

        # Show the app landing page 
        @app.event("app_home_opened")
        def app_home_opened(client, event, logger):
            on_home_opened(client, event, logger)

        # Open Change Request modal
        @app.action("change_request")
        def open_change_request(ack, body, client, logger):
            on_change_request_opened(ack, body, client, logger)

        # Update Change Request modal with available environments
        @app.action("selection_domain")
        def selection_domain(ack, body, client, logger):
            on_domain_selected(ack, body, client, logger)

        # Update Change Request modal with available domain groups
        @app.action("selection_environment")
        def selection_environment(ack, body, client, logger):
            on_environment_selected(ack, body, client, logger)
            
        # Update Change Request modal with available group switchers
        @app.action("selection_group")
        def selection_group(ack, body, client, view, logger):
            on_group_selected(ack, body, client, logger)

        # Update Change Request modal with status options
        @app.action("selection_switcher")
        def selection_switcher(ack, body, client, logger):
            on_switcher_selected(ack, body, client)

        # Confirm status selection
        @app.action("selection_status")
        def selection_status(ack, body, client, logger):
            ack()

        # Submit Change Request for review
        @app.view("change_request_review")
        def handle_change_request_review(ack, body, client, view, logger):
            on_change_request_review(ack, body, client, view, logger)

        # Submit Change Request for verification and approval
        @app.action("change_request_submit")
        def handle_submission(ack, body, client, view, logger):
            on_submit(ack, body, client, logger)

        # Abort Change Request
        @app.action("change_request_abort")
        def handle_change_request_abort(ack, body, client, view, logger):
            on_change_request_abort(ack, body, client)

        # Request approved
        @app.action("request_approved")
        def request_approved(ack, body, client, logger):
            on_request_approved(ack, body, client, logger)

        # Request denied
        @app.action("request_denied")
        def request_denied(ack, body, client, logger):
            on_request_denied(ack, body, client, logger)