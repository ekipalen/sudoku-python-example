from time import sleep
from robocorp import browser
from robocorp.tasks import task

URL = "https://www.nytimes.com/puzzles/sudoku/easy"
EMPTY_CELLS_LOCATOR = "//div[@data-cell and not(contains(@class, 'su-cell prefilled'))]"

@task
def solve_challenge():
    """Solve the Sudoku challenge"""
    empty_cells = open_browser_to_the_sudoku_challenge()
    completed = False
    while not completed:
        empty_cells, completed = try_the_numbers(empty_cells)
    sleep(5)

def open_browser_to_the_sudoku_challenge():
    browser.configure(
        browser_engine="chromium",
        screenshot="only-on-failure",
        headless=False,
    )
    
    page = browser.goto(URL)
    page.wait_for_selector("//button[contains(text(),'Continue')]").click()
    page.wait_for_selector("//button[@id='pz-gdpr-btn-accept']").click()
    page.wait_for_selector("//button[contains(text(),'Normal')]").click()
    sleep(3)
    locator = browser.page().locator(EMPTY_CELLS_LOCATOR)
    empty_cells = locator.element_handles()
    return empty_cells

def try_the_numbers(empty_cells):
    new_list_of_empty_cells = []
    for cell in empty_cells:
        possible_numbers = []
        cell.click(force=True)
        for number in range(1, 10):
            cell.press(str(number))
            error = browser.page().locator("//div[@class='su-cell guessed selected conflicted']").count()
            if error == 0:
                possible_numbers.append(number)
        if len(possible_numbers) == 1:
            cell.press(str(possible_numbers[0]))
        else:
            new_list_of_empty_cells.append(cell)
            cell.press('Backspace')

    element = browser.page().locator("//div[@class='xwd__modal--body modal-congrats-body animate-opening']").count()
    completed = True if element == 1 else False
    return new_list_of_empty_cells, completed