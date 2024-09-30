<H3>Atividade de FullStack</H3>

<p>CRIAR PRODUTO:</p> curl -X POST http://127.0.0.1:5001/product -H "Content-Type: application/json" -d "{\"name\": \"Cerveja\", \"stock\": 20, \"price\": 29.99}"

REALIZAR VENDA: curl -X POST http://127.0.0.1:5001/sale -H "Content-Type: application/json" -d "{\"user_id\": 1, \"product_id\": 1, \"quantity\": 7}"

DELETAR PRODUTO: curl -X DELETE http://127.0.0.1:5001/product/2

