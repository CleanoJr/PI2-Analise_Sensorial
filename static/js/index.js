const express = require("express");
const cors = require("cors");
const app = express();
const port = 9000;

const usuarioRoutes = require('./src/routes/usuarioRoutes');

app.use(express.json());
app.use(cors());

app.get("/", (req, res) => {
  res.send("API do Museu");
});

app.use("/usuarios", usuarioRoutes);

app.listen(port, () => {
  console.log(`Servidor rodando na porta: http://localhost:${port}`);
});