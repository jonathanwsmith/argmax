from requests import Session

from argmax.exception.stack_overflow_exception import StackOverflowException
from argmax.model.stack_overflow_response import StackOverflowResponse


class StackOverflow:

    def __init__(self):
        self.s = Session()

    def lookup_users(self) -> StackOverflowResponse:
        response = self.s.request("GET",
                                  url="https://api.stackexchange.com/2.2/users?page=1&pagesize=10&site=stackoverflow")
        model: StackOverflowResponse = StackOverflowResponse.model_validate(response.json())

        if model.error_id is None:
            return model
        else:
            raise StackOverflowException(model.error_id, model.error_message)


if __name__ == "__main__":
    s = StackOverflow()
    users = s.lookup_users()
    print(users)
