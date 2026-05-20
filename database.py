import aiosqlite

DB_NAME = "shop.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                price INTEGER,
                photo TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER,
                quantity INTEGER
            )
        """)
        await db.commit()

async def get_products():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT * FROM products")
        return await cursor.fetchall()

async def add_to_cart(user_id, product_id, quantity=1):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT id, quantity FROM cart WHERE user_id = ? AND product_id = ?",
            (user_id, product_id)
        )
        item = await cursor.fetchone()
        if item:
            cart_id, old_qty = item
            await db.execute("UPDATE cart SET quantity = ? WHERE id = ?", (old_qty + quantity, cart_id))
        else:
            await db.execute("INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)", (user_id, product_id, quantity))
        await db.commit()

async def get_cart(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT products.name, products.price, cart.quantity
            FROM cart JOIN products ON cart.product_id = products.id
            WHERE cart.user_id = ?
        """, (user_id,))
        return await cursor.fetchall()

async def clear_cart(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
        await db.commit()