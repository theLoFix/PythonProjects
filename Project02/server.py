import mymath
from fastapi import FastAPI, Header, HTTPException
from typing import List, Annotated

app = FastAPI()


@app.post("/sum")
def api_sum(
    lst: List[int | float],
    api_key: Annotated[str, Header()]
):
    """
    Calculate the sum of a list of numbers.
    """
    
    if api_key != "TAJNEHASLO" :
        return HTTPException(
            status_code=403,
            detail="Invalid API key"
        )

    return {
        "result": mymath.my_sum(lst)
    }