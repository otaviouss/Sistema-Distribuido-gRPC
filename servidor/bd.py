import asyncio

from prisma import Prisma

class banco():

    async def inserir_usuario(email, nome, senha) -> int:
        prisma = Prisma()
        await prisma.connect()

        user = await prisma.usuario.create(
            data={
                'email': email,
                'nome': nome,
                'senha': senha,
            }
        )

        await prisma.disconnect()

        return user.id
    
    async def ver_usuario(email, senha) -> None:
        prisma = Prisma()
        await prisma.connect()

        user = await prisma.usuario.find_first(
            where={
                'email': email,
                'senha': senha,
            }
        )

        await prisma.disconnect()

        return user
    
    async def ver_usuarios() -> None:
        prisma = Prisma()
        await prisma.connect()

        users = await prisma.usuario.find_many()

        await prisma.disconnect()

    async def inserir_voucher(titulo, descricao, gato, local, lanche, duracao, imagem, titular_id) -> int:
        prisma = Prisma()
        await prisma.connect()

        voucher = await prisma.voucher.create(
            data={
                'titulo': titulo, 
                'descricao': descricao,
                'gato': gato,
                'local': local,
                'lanche': lanche,
                'duracao': duracao,
                'imagem': imagem,
                'titular_id': titular_id,
            }
        )

        await prisma.disconnect()

        return voucher.id

    async def ver_vouchers() -> None:
        prisma = Prisma()
        await prisma.connect()

        vouchers = await prisma.voucher.find_many(
            include={
                'titular': True,
                'Troca1': True,
                'Troca2': True,
            }
        )

        await prisma.disconnect()

        return vouchers

    async def ver_vouchers_usuario(id_usuario) -> None:
        prisma = Prisma()
        await prisma.connect()

        vouchers = await prisma.voucher.find_many(
            where={
                'titular_id': id_usuario,
            }
        )

        await prisma.disconnect()

        return vouchers
    
    async def alterar_Titular_Voucher(id, novo_titular_id) -> None:
        prisma = Prisma()
        await prisma.connect()

        voucher = await prisma.voucher.update(
            data={
                'titular_id': novo_titular_id,
            },
            where={
                'id': id,
            }
        )

        await prisma.disconnect()

    async def nova_Troca(id_v1, id_v2) -> int:
        prisma = Prisma()
        await prisma.connect()

        troca = await prisma.troca.create(
            data={
                'voucher1_id': id_v1,
                'voucher2_id': id_v2,
                'status': 0,
            }
        )

        await prisma.disconnect()

        return troca.id

    async def ver_Trocas() -> None:
        prisma = Prisma()
        await prisma.connect()

        trocas = await prisma.troca.find_many(
            include={
                'v1': True,
                'v2': True,
            }
        )

        await prisma.disconnect()

        return(trocas)

    async def alterar_Status_Troca_Aceito(id) -> None:
        prisma = Prisma()
        await prisma.connect()

        troca = await prisma.troca.update(
            data={
                'status': 1,
            },
            where={
                'id': id,
            },
            include={
                'v1': True,
                'v2': True,
            }
        )

        await prisma.voucher.update(
            data={
                'titular_id': troca.v2.titular_id,
            },
            where={
                'id': troca.v1.id,
            }
        )

        await prisma.voucher.update(
            data={
                'titular_id': troca.v1.titular_id,
            },
            where={
                'id': troca.v2.id,
            }
        )

        await prisma.troca.update_many(
            data={
                'status': 2,
            },
            
            where={
                'OR': [
                    {
                        'voucher1_id': troca.v1.id,
                    },
                    {
                        'voucher2_id': troca.v2.id,
                    },
                ],
                'NOT': [
                    {
                        'status': 1,
                    },
                ],
            }
        )

        await prisma.disconnect()
    
    async def alterar_Status_Troca_Rejeitado(id) -> None:
        prisma = Prisma()
        await prisma.connect()

        troca = await prisma.troca.update(
            data={
                'status': 2,
            },
            where={
                'id': id,
            }
        )

        await prisma.disconnect()
    
    async def id_usuario_by_email(email) -> None:
        prisma = Prisma()
        await prisma.connect()

        user = await prisma.usuario.find_first(
            where={
                'email': email,
            }
        )

        await prisma.disconnect()

        return user.id
    

if __name__ == '__main__':
    #u = asyncio.run(banco.inserir_usuario("fabi@hotmail.com", "Fábio", "123"))
    #asyncio.run(banco.inserir_voucher("V1", "D1", "Belinha", "Sala", "Ração", "", "URL", u))
    #asyncio.run(banco.nova_Troca(3, 4))
    #asyncio.run(banco.ver_usuarios())
    u = asyncio.run(banco.ver_usuario("fabi@hotmail.com", "123"))
    print(u)
    v=asyncio.run(banco.ver_vouchers())
    print(v)
    #asyncio.run(banco.alterar_Status_Troca_Rejeitado(1))
    #asyncio.run(banco.ver_Trocas())
    #asyncio.run(banco.alterar_Status_Troca_Aceito(8))


