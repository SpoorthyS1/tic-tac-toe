import os
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uuid
import prog1

# simple API key guard
API_KEY = os.environ.get("API_KEY")

def verify_api_key(x_api_key: str | None = Header(None)):
    if not API_KEY:
        return True
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return True

# Create app WITHOUT global dependency
app = FastAPI(title="LetMeKnow TicTacToe API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GAMES = {}

class CreateGameReq(BaseModel):
    human_symbol: str = "X"
    ai_difficulty: str = "medium"

class MoveReq(BaseModel):
    row: int
    col: int

# Serve the HTML game interface
@app.get("/")
def read_root():
    return FileResponse('static/index.html')

# Protected endpoints (add dependency to each if you want API key)
@app.post("/games")
def create_game(req: CreateGameReq):
    game = prog1.create_game(human_symbol=req.human_symbol, ai_difficulty=req.ai_difficulty)
    game_id = str(uuid.uuid4())
    GAMES[game_id] = game
    return {"game_id": game_id, "state": game['get_state']()}

@app.get("/games/{game_id}/state")
def get_state(game_id: str):
    game = GAMES.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return {"state": game['get_state']()}

@app.post("/games/{game_id}/move")
def make_move(game_id: str, req: MoveReq):
    game = GAMES.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    result = game['make_move'](req.row, req.col)
    return {"result": result, "state": game['get_state']()}

@app.post("/games/{game_id}/reset")
def reset_game(game_id: str):
    game = GAMES.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game['reset']()