import simpy
import random
import statistics


class CallCenter(object):
    def __init__(self, env, technicians):
        self.env = env
        self.technician = simpy.Resource(env, technicians)

    def assist_customer(self, customer):
        yield self.env.timeout(random.randint(45, 60))


def customer_call(env, customer, call_center):
    arrival_time = env.now

    with call_center.technician.request() as call:
        yield call
        start_service = env.now
        yield env.process(call_center.assist_customer(customer))

    wait_times.append(start_service - arrival_time)


def run_call_center(env, technicians):
    call_center = CallCenter(env, technicians)
    customer = 0

    while True:
        yield env.timeout(random.randint(10, 20))
        customer += 1
        env.process(customer_call(env, customer, call_center))


if __name__ == '__main__':
    wait_times = []
    env = simpy.Environment()
    env.process(run_call_center(env, 4))
    env.run(until=10000)
    print(statistics.mean(wait_times))
    print(statistics.variance(wait_times))


