#!/usr/bin/env python

from fastapi import FastAPI
import sys
from rest import set_test_mode, router


app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    set_test_mode(len(sys.argv) > 1 and sys.argv[1] == 'test')
