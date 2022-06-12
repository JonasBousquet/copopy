import time

start = time.time()
# ^ put this at the start

# for i in range(1999):
#    print(i)

# put this at the end of your code
end = time.time()
zeit = end - start
if zeit > 60:
    minutes = int(zeit / 60)
    sec = zeit % 60
    sec = round(sec, 2)
    print(f'\n[Finished in  {minutes} m and {sec} s]')
else:
    zeit = round(zeit, 2)
    print(f'\n[Finished in {zeit} s]')
