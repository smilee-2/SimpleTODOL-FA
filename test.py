import flet as ft
import flet_fastapi
import uvicorn


async def main(page: ft.Page):
    async def add_clicked(e):
        await page.add_async(ft.Checkbox(label=new_task.value))
        new_task.value = ""
        await page.update_async()

    new_task = ft.TextField(hint_text="What's needs to be done?")



    await page.add_async(
        new_task,
        ft.IconButton(icon=ft.icons.ADD, on_click=add_clicked)
    )



app = flet_fastapi.app(main)

if __name__ == '__main__':

    uvicorn.run("test:app")


