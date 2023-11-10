suppressMessages({
    library(ggplot2)
    library(gridExtra)
    library(dplyr)
    library(scales)
    library(viridis)
})


genPlot <- function(data, name, title, color) {
    plot <- ggplot(data, aes(x = timestamp)) +
        geom_line(aes(y = .data[[name]]), size = 0.3, color = color, show.legend = FALSE) +
        scale_x_continuous("Elapsed Time [sec]") +
        scale_y_continuous("RAM Usage", labels = label_bytes(units = "MB"),
            limits = c(0, 2.5e+09)) +
        theme(
            plot.title = element_text(size = 8, color = color, hjust = 0.5),
            axis.title = element_text(size = 5,face = "bold"),
            axis.text = element_text(size = 5)
        ) +
        ggtitle(title)
    return(plot)
}

plotData <- function(src_file, dst_file) {
    data <- read.csv(src_file, header = TRUE, sep = "\t")

    data <- data %>%
        mutate(timestamp = (timestamp - min(timestamp))/1000)

    colors = magma(5)[2:4]
    p1 = genPlot(data, "fragment_metadata", "FragmentMetadata", colors[1])
    p2 = genPlot(data, "reader", "Reader", colors[2:2])
    p3 = genPlot(data, "writer", "Writer", colors[3])
    p4 = grid.arrange(p1, p2, p3, nrow = 3)
    ggsave(dst_file, plot = p4, device = "jpeg", width = 8, height = 4)
}

plotData("data/import.csv", "data/import.jpg")
plotData("data/consolidation.csv", "data/consolidation.jpg")


