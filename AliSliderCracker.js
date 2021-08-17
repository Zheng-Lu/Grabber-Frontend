const puppeteer = require('puppeteer')

async function bypass(){
    const  browser = await puppeteer.launch({
        headless: false, //
        defaultViewport: {width:1366, height:768}
    })
    const page = await browser.newPage()

    await page.evaluateOnNewDocument(() => {
        Object.defineProperty(navigator, 'webdriver',{
            get: () => false
        })
    })

    //Login page
    await page.goto('https://login.aliexpress.com')

    //Input email and password
    await page.click('input#fm-login-id.fm-text')
    await page.keyboard.type('Lz429671594@outlook.com');
    await page.click('input#fm-login-password.fm-text');
    await page.keyboard.type('pf52CE4JyGiY7fj');
    await page.click('.fm-button')

    // let sliderElement = await page.$('span.btn_slide')

    await page.waitForSelector('.nc_iconfont.btn_slide', {timeout: 30000})

    const sliderElement = await page.$('.slidetounlock')
    const slider = await sliderElement.boundingBox()

    const sliderHandle = await page.$('.nc_iconfont.btn_slide')
    const handle = await sliderHandle.boundingBox()

    await page.mouse.move(handle.x + handle.width / 2, handle.y + handle.height / 2)
    await page.mouse.down()
    await page.mouse.move(handle.x + slider.width, handle.y + handle.height / 2, {steps:50})
    await page.mouse.up()

    await page.waitForNavigation({
        waitUntil: 'load'
    });

    await browser.close()
}

async function googleLogin(){
    const  browser = await puppeteer.launch({
        headless: false,
        defaultViewport: {width:1366, height:768}
    })
    const page = await browser.newPage()

    await page.evaluateOnNewDocument(() => {
        Object.defineProperty(navigator, 'webdriver',{
            get: () => false
        })
    })

    //Login page
    await page.goto('https://login.aliexpress.com')

    await page.click('a.fm-sns-item.google')

}


// googleLogin()
bypass()