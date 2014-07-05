
package org.hagiasmon.threads;

/**
 * Simple demo of threads.
 *
 * @author wbmccarty
 *
 * For more information on threads, see Goetz, B., & Peierls, T. (2010). <i>Java Con-
 * currency in Practice</i>. N.p.: Pearson Education. Retrieved from 
 * <a href="http://my.safaribooksonline.com/book/programming/java/0321349601">
 * http://my.safaribooksonline.com/book/programming/java/0321349601</a>.
 *
 */
public class ThreadDemo {

    /**
     * Inner class HelloThread, a subclass of Thread.
     *
     */
    public class HelloThread extends Thread {

        /**
         * Used to pause a thread.
         */
        protected static final int SLEEP_DURATION = 4000;

        /**
         * Used to identify/describe a HelloThread instance.
         */
        private final String threadname;

        /**
         * Construct a HelloThread object.
         *
         * @param tn name used to identify/describe a HelloThread instance.
         */
        public HelloThread(final String tn) {
            threadname = tn;
        }

        /**
         * Get the string used to identify/describe the HelloThread instance.
         *
         * @return the descriptive string.
         */
        public final String getThreadName() {
            return threadname;
        }

        /**
         * Method associated with the runnable interface required of a Thread.
         * The start() method is used to initiate thread execution. The run()
         * method is used internally and is not called by the program.
         */
        @Override
        public final void run() {
            System.out.printf("Hello from thread %s!\n", getThreadName());

            // Sleep for a bit, unless interrupted.
            try {
                Thread.sleep(SLEEP_DURATION);
            } catch (final InterruptedException e) {
                System.out.printf(
                        "Notification from thread %s: I was interrupted!\n",
                        getThreadName());
                // Set the flag asking the thread to interrupt itself,
                // which is cleared by the thrown exception.
                Thread.currentThread().interrupt();
            }
            System.out.printf("Goodbye from thread %s!\n", getThreadName());
        }
    }

    /**
     * Value used to pause a thread.
     */
    protected static final int SLEEP_DURATION = 1000;

    /**
     * This method is called by the OS to initiate the program.
     *
     * @param args Not used
     */
    public static void main(final String[] args) {
        System.out.println("Hello, World!");
        final ThreadDemo tb = new ThreadDemo();

        // Create the HelloThread instances
        final HelloThread[] threads = new HelloThread[2];
        threads[0] = tb.threadFactory("t0");
        threads[1] = tb.threadFactory("t1");

        // Start the threads
        for (final HelloThread t : threads) { t.start(); }

        try {
            // Sleep for a bit and then interrupt thread #1
            Thread.sleep(SLEEP_DURATION);
            threads[1].interrupt();

            // Join the threads, waiting until they finish.
            for (final HelloThread t : threads) { t.join(); }
        } catch (InterruptedException e) {
            for (final HelloThread t : threads) {
                if (t.isInterrupted()) {
                    System.out.printf("Thread interrupted: %s\n",
                    t.getThreadName());
                }
            }
        }

        System.out.println("Goodbye, World!");
    }

    /**
     * Factory method used to obtain a HelloThread instance.
     *
     * @param tn the desired thread name
     * @return the HelloThread instance
     */
    public final HelloThread threadFactory(final String tn) {
        return new HelloThread(tn);
    }
}
