import requests
from bs4 import BeautifulSoup, SoupStrainer
from dataclasses import dataclass

@dataclass
class Piece:
    id:str
    name:str
    total_quantity:int
    used_quantity:int
    img_url:str
    piece_url:str

def get_pieces() -> dict[str, Piece]:
    lego_id = input('What is the lego id ? : ')
    BASE_URL = 'https://www.bricklink.com'
    pieces:dict[str, Piece] = {}

    soup = BeautifulSoup(requests.get(
        f'{BASE_URL}/catalogItemInv.asp?S={lego_id}-1',
        headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0'}
    ).content, 'lxml', parse_only=SoupStrainer({'tr': {'class':'IV_ITEM'}}))

    for piece in soup.select('tr.IV_ITEM'):
        id = piece['class'][0].replace('IV_', '')
        quantity = int(piece.select_one('td[align="RIGHT"]').text.strip())
        try: pieces[id].total_quantity += quantity
        except: pieces[id] = Piece(
            id, piece.select('td')[3].text,
            quantity,
            quantity,
            piece.select_one('img')['src'],
            BASE_URL + piece.select_one('a')['href']
        )

    return pieces

def pieces_to_csv(pieces:dict[str, Piece]) -> str:
    DELIMITER = '; '
    pieces_csv = DELIMITER.join(Piece.__annotations__.keys())+'\n'
    for piece in pieces.values(): pieces_csv += DELIMITER.join(map(str, vars(piece).values())) + '\n'
    with open('pieces.csv', 'w+', encoding='utf-8') as f: f.write(pieces_csv)
    
    return pieces_csv

if __name__ == '__main__':
    pieces = get_pieces()
    print(pieces_to_csv(pieces))