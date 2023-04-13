import aiohttp
import asyncio
import aioconsole

async def main():
    async with aiohttp.ClientSession('http://localhost:8080') as session:
        while(True):
            prompt = ''' Enter Action: 
1. disc
2. alreadySub
3. sub
4. unsub
5. getDat
        '''
            selection = await aioconsole.ainput(prompt)
            await asyncio.sleep(2)
        
            if selection == 'disc':
                async with session.get('/ingester/discover') as resp:
                    print(resp.status)
                    nodes = await resp.text()
                    print(nodes)
            elif selection == 'alreadySub':
                async with session.get('/ingester/subscribed') as resp:
                    print(resp.status)
                    subscribed_nodes = await resp.text()
                    print(subscribed_nodes)
                    nodesub = '8090'
            elif selection == 'sub':
                subscribe_to_node = await aioconsole.ainput("Enter node to sub")
                async with session.get('/ingester/subscribe/'+ subscribe_to_node) as resp:
                    print(resp.status)
                    nodes_sub = await resp.text()
                    print('subsbribed to node' + nodes_sub)
                    await asyncio.sleep(1)
            elif selection == 'unsub':
                unsubscribe_to_node = await aioconsole.ainput("Enter node to unsub")
                async with session.get('/ingester/unsubscribe/'+ unsubscribe_to_node) as resp:
                    print(resp.status)
                    nodes_sub = await resp.text()
                    print('subsbribed to node' + nodes_sub)      
            elif selection == 'getDat':
                async with session.ws_connect('/hub/dashboard') as ws:
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            if msg.data == 'close cmd':
                                await ws.close()
                                break
                            else:
                                try:
                                    async with asyncio.timeout(0.25):
                                        # serv_response = await ws_serv.receive()
                                        print(msg.data)
                                        break
                                except TimeoutError:
                                    continue
                        #         print(msg.data)
                        #         await asyncio.sleep(5)
                        # elif msg.type == aiohttp.WSMsgType.ERROR:
                        #     break 
            else:
                print("not valid selection")
asyncio.run(main())