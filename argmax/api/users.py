import pydantic_core
from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse

from argmax.exception.unsupported_type_exception import UnsupportedTypeException
from argmax.model import UsersResponse, DetectionResult, UsersRequest
from argmax.so import StackOverflow
from argmax.util import Detection

router = APIRouter()
so = StackOverflow()
detection = Detection()


@router.post("/users")
def get_users(body: UsersRequest = Body()):
    try:
        if body.query is None or len(body.query) == 0:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "The query parameter 'query' must be present and non empty."})

        user_lookup = so.lookup_users()
        dl = []
        for u in user_lookup.items:
            try:
                boxes, time = detection.find(str(u.profile_image), body.query)
            except UnsupportedTypeException as e:
                return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"error":f"{e}"})

            dl.append(DetectionResult(user_id=u.user_id, display_name=u.display_name, profile_image=str(u.profile_image), object_detected=len(boxes) > 0, detection_time_ms=time, bounding_boxes=boxes))

        return UsersResponse(items=dl)

    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": f"{e}"})


# Development testing scaffold
if __name__ == "__main__":
    import json
    ur = UsersRequest(query="person")
    users = get_users(ur)
    print(json.dumps(pydantic_core.to_jsonable_python(users), indent=2))
